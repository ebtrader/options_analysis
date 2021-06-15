import yfinance as yf
import pandas as pd
import numpy as np
import timeit

from datetime import datetime as dt

from scipy.stats import norm

start = timeit.default_timer()

# https://algotrading101.com/learn/yfinance-guide/

#https://aroussi.com/post/download-options-data

#prompt for a symbol
symbol = input('What is your stock ticker?:  ')
min_delta = float(input('what is the minimum delta(e.g. 0.7 is 70%)?:   '))
min_yield = float(input('what is the minimum weekly yield (e.g. .01 is 1%)?:   '))
max_expiration = input('what is the latest expiration?(mm-dd-yyyy):   ')

#hard-wire a symbol without the prompt

#symbol = 'Tna'

#print symbol
#print(symbol.upper())

#yfinance version of your symbol
ticker = yf.Ticker(symbol)

# print descriptive info about the ticker
#print(ticker.info)

#historical prices
#historical = ticker.history(start="2020-12-02", end="2020-12-04", interval="5m")
#print(historical)

#how far back you go - period
# “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

#bars or candles - interval
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

#hist = ticker.history(period="3d", interval = "5m")
#print(hist)

#multiple_tickers = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
#print(multiple_tickers)

#multi_ticker_history = yf.download("AMZN AAPL GOOG", period="3d", interval = "5m")
#print(multi_ticker_history)

#options

#pull in the entire options chain for one expiration
#expiration = input('What is your expiration date? (yyyy-mm-dd):  ')
#expiration = '2021-01-08'

#exp_dates = []
exp_dates = ticker.options # this is the list of expiration dates
#print(exp_dates)
#opt = ticker.option_chain(expiration)
#print(opt)

#opt = ticker.option_chain(exp_dates)

df = pd.DataFrame()
for x in exp_dates:
    opt = ticker.option_chain(x)
    df = df.append(opt.calls, ignore_index=True)


#df = pd.DataFrame(opt.calls)

hist = ticker.history(period="3d", interval = "5m")
#print(hist)
df_history = pd.DataFrame(hist)
recent_value = df_history['Close'].iloc[-1]
print(recent_value)

df['recent_px'] = recent_value

#df['recent_px'] = 173.75


#intrinsic value = stock price - strike price

df['intrinsic_value'] = df['recent_px'] - df['strike']
df['intrinsic_value'] = np.where(df['intrinsic_value'] < 0, 0, df['intrinsic_value'])

#option price = mid
#mid = (bid + ask) / 2

df['option_px'] = (df['bid'] + df['ask']) / 2 #mid options price

#extrinsic value = option price - intrinsic value

df['extrinsic_value'] = df['option_px'] - df['intrinsic_value']
df['extrinsic_value'] = np.where(df['extrinsic_value'] < 0, 0, df['extrinsic_value'])

#yield = ( extrinsic / recent_px ) * 100

df['yield'] = (df['extrinsic_value'] / df['recent_px'] )

#contract_symbol = str(df['contractSymbol'].iloc[0])
#print(contract_symbol)
#beginning_index = contract_symbol.find('2')
#print(beginning_index)
#ending_index = beginning_index + 6
#print(ending_index)
#expiration_slice = contract_symbol[beginning_index:ending_index]
#print(expiration_slice)

df['contract_symbol'] = df['contractSymbol'].astype(str)
df['beginning_index'] = (df['contract_symbol'].str.find('2'))
df['ending_index'] = (df['beginning_index'] + 6)
begin_index = df['beginning_index'].iloc[0]
end_index = df['ending_index'].iloc[0]
df['expiration_slice'] = df['contract_symbol'].str.slice(begin_index,end_index)

todays_date = pd.to_datetime('today')
df['today'] = todays_date

df['expiration_combined'] = '20' + df['expiration_slice']
df['converted_expiration'] = pd.to_datetime(df['expiration_combined'])
df['days_to_expiration'] = (df['converted_expiration'] - df['today']).dt.days

#number of weeks
df['number_of_weeks'] = df['days_to_expiration'] / 7

#weekly yield
df['weekly_yield'] = np.where( df['number_of_weeks'] < 1, df['yield'],  df['yield'] / df['number_of_weeks'])

# Greeks
df['T'] = df['days_to_expiration'] / 200

risk_free_rate = 0.00
df['r'] = risk_free_rate

df['v'] = df['impliedVolatility']
dividend_rate = .00
df['d'] = dividend_rate
df['S'] = df['recent_px']
df['K'] = df['strike']

df['T_sqrt'] = np.sqrt(df['T'])

df['d1'] = (np.log(df['S'].astype(float) / df['K']) + (( df['r'] - df['d'] ) + df['v'] * df['v'] / 2)  * df['T'] )  / (df['v'] * df['T_sqrt'])
df['delta_calc'] = norm.cdf(df['d1'])

#jjj score
df['jjj'] = df['weekly_yield'] * df['delta_calc']


# df['d2'] = df['d1'] - df['v'] * df['T_sqrt']
#
# df['gamma'] = norm.pdf(df['d1']) / (df['S'] * df['v'] * df['T_sqrt'])
#
# df['theta'] = -(df['S'] * df['v'] * norm.pdf(df['d1'])) / (2 * df['T_sqrt']) - df['r'] * df['K'] * np.exp(-df['r'] * df['T']) * norm.cdf(df['d2'])
#
# df['vega'] = df['S'] * df['T_sqrt'] * norm.pdf(df['d1'])
#
# df['rho'] = df['K'] * df['T'] * np.exp(-df['r'] * df['T']) * norm.cdf(df['d2'])

#print(df)

#df.to_csv("greeks.csv")

#dfobj = df[['delta_calc', 'strike']]
#dfobj.to_csv('just_delta_strike.csv')

df_two_colums = df[['strike','delta_calc', 'yield', 'converted_expiration', 'weekly_yield', 'jjj' ]]
#print(df_two_colums)
df_two_colums.to_csv('two_columns.csv')

#filters out for delta threshold

find_delta = df_two_colums.loc[lambda df_two_columns: df_two_columns['delta_calc'] > min_delta, :]
#print(find_delta)
#find_delta.to_csv('find_delta.csv')

#filters out for expiration threshold
find_delta_first_expiration = find_delta.loc[lambda find_delta: find_delta['converted_expiration'] <= max_expiration, :]
#print(find_delta_first_expiration)

#filters out for yield threshold
#find_delta_and_yield = find_delta_first_expiration.loc[lambda find_delta_first_expiration: find_delta_first_expiration['yield'] > .008, :]

find_delta_and_yield = find_delta_first_expiration.loc[lambda find_delta_first_expiration: find_delta_first_expiration['weekly_yield'] > min_yield, :]
# find_delta_and_yield = find_delta.loc[lambda find_delta: find_delta['yield'] > .04, :]
print(find_delta_and_yield)
find_delta_and_yield.to_csv('find_delta_and_yield.csv')

#chooses the strike with the max yield
#max_value = find_delta_and_yield['yield'].max()
max_value = find_delta_and_yield['weekly_yield'].max()
print(max_value)

find_final_strike = find_delta_and_yield.loc[lambda find_delta_and_yield: find_delta_and_yield['weekly_yield'] == max_value, :]
print(find_final_strike)

stop = timeit.default_timer()

print('Time: ', stop - start)