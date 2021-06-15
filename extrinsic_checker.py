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
# symbol = input('What is your stock ticker?:  ')
# min_delta = float(input('what is the minimum delta(e.g. 0.7 is 70%)?:   '))
# min_yield = float(input('what is the minimum weekly yield (e.g. .01 is 1%)?:   '))
# max_expiration = input('what is the latest expiration?(mm-dd-yyyy):   ')


symbol = 'TQQQ'
ticker = yf.Ticker(symbol)

# how far back you go - period
# “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

# bars or candles - interval
# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

#options

#exp_dates = []
# exp_dates = ticker.options # this is the list of expiration dates

# print(exp_dates)
#opt = ticker.option_chain(expiration)
#print(opt)

#opt = ticker.option_chain(exp_dates)


df = pd.DataFrame()
exp_dates = '2021-06-18'
opt = ticker.option_chain(exp_dates)
df = df.append(opt.calls, ignore_index=True)

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

# https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values

selected_strike = 100

selected_row = df.loc[df['strike'] == selected_strike]
print(selected_row)

selected_extrinsic = selected_row['extrinsic_value'].values[0]

print(selected_extrinsic)

if selected_extrinsic > 0.3:
    print('extrinsic is still too high!')
else:
    print('time to roll')

# print(df)

# df.to_csv('extrinsic_checker.csv')

