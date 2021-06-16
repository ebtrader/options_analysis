import smtplib, ssl
import time

# use outlook app and put it in favorites by selecting the sender email address and clicking star in upper-right
# then set notifications for favorites

class EmailYahoo:

    def __init__(self):
        self.counter = 0
        self.buy_msg = "Buy today"


    def email_func(self):

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "jmzakatees@gmail.com"
        receiver_email = 'crudedecay@gmail.com'
        password = 'suite203!'

        message = f'''\
        From: Javed Siddique {sender_email}
        To: Javed Siddique {receiver_email}
        Subject: {self.buy_msg}


        Dear Javed, This trigger {self.buy_msg} will execute only once\

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
        x = 0
        while self.counter < 10:
            x = x + 1
            print(x)
            if x == 3:
                self.buy_msg = "Short that mutha!"
                self.email_func()
            else:
                time.sleep(10)
                self.counter += 1

def main():
    app = EmailYahoo()
    app.trigger()

if __name__ == "__main__":
    main()