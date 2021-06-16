import smtplib, ssl
import time
import yfinance as yf
import pandas as pd
import numpy as np

# use outlook app and put it in favorites by selecting the sender email address and clicking star in upper-right
# then set notifications for favorites

class EmailYahoo:

    def email_func(self):
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "jmzakatees@gmail.com"
        receiver_email = 'crudedecay@gmail.com'
        password = 'suite203!'

        message = f'''\
        From: Javed Siddique {sender_email}
        To: Javed Siddique {receiver_email}
        Subject: Only one trigger


        Dear Javed, Roll that option!\

        '''

        # send email here

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print('It did not work!')
            print(e)
        finally:
            server.quit()

    def trigger(self):
        symbol = 'TQQQ'
        exp_dates = '2021-06-18'
        selected_strike = 105
        threshold = 0.2

        # symbol = 'TQQQ'
        ticker = yf.Ticker(symbol)

        # how far back you go - period
        # “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

        # bars or candles - interval
        # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

        # options

        # exp_dates = []
        # exp_dates = ticker.options # this is the list of expiration dates

        # print(exp_dates)
        # opt = ticker.option_chain(expiration)
        # print(opt)

        # opt = ticker.option_chain(exp_dates)

        df = pd.DataFrame()
        # exp_dates = '2021-06-18'
        opt = ticker.option_chain(exp_dates)
        df = df.append(opt.calls, ignore_index=True)

        hist = ticker.history(period="3d", interval="5m")
        # print(hist)
        df_history = pd.DataFrame(hist)
        recent_value = df_history['Close'].iloc[-1]
        print(f'recent price = {recent_value:.2f}')

        df['recent_px'] = recent_value

        # df['recent_px'] = 173.75

        # intrinsic value = stock price - strike price

        df['intrinsic_value'] = df['recent_px'] - df['strike']
        df['intrinsic_value'] = np.where(df['intrinsic_value'] < 0, 0, df['intrinsic_value'])

        # option price = mid
        # mid = (bid + ask) / 2

        df['option_px'] = (df['bid'] + df['ask']) / 2  # mid options price

        # extrinsic value = option price - intrinsic value

        df['extrinsic_value'] = df['option_px'] - df['intrinsic_value']
        df['extrinsic_value'] = np.where(df['extrinsic_value'] < 0, 0, df['extrinsic_value'])

        # yield = ( extrinsic / recent_px ) * 100

        df['yield'] = (df['extrinsic_value'] / df['recent_px'])

        # https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values

        # selected_strike = 100

        selected_row = df.loc[df['strike'] == selected_strike]
        print(selected_row)

        selected_extrinsic = selected_row['extrinsic_value'].values[0]

        print(f'current extrinsic = {selected_extrinsic:.2f}')

        counter = 0
        while counter < 5:

            if selected_extrinsic < threshold:
                print('time to roll!')
                self.email_func()
                time.sleep(30)
                counter += 1
            else:
                time.sleep(30)
                print('extrinsic is still too high!')
                counter += 1
        # print(df)

        # df.to_csv('extrinsic_checker.csv')


def main():
    app = EmailYahoo()
    app.trigger()

if __name__ == "__main__":
    main()