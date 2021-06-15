import yfinance as yf
import pandas as pd
import numpy as np

# https://algotrading101.com/learn/yfinance-guide/

#https://aroussi.com/post/download-options-data


# “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

ticker = yf.Ticker("TQQQ")
#aapl_historical = aapl.history(start="2020-12-02", end="2020-12-04", interval="5m")
#print (aapl_historical)

multiple_tickers = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
#print(multiple_tickers)

#print (aapl.options)

opt = ticker.option_chain('2020-12-11')
#print(opt.calls)
#print(opt.puts)

df = pd.DataFrame(opt.calls)
#print(df)

#for col in df.columns:
#    print(col)

#df.to_csv('options_chain.csv')

hist = ticker.history(period="3d", interval = "5m")
#print(hist)

df_history = pd.DataFrame(hist)
df_history.to_csv('price_history.csv')
recent_price = df_history['Close'].iloc[-1]
print(recent_price)

#df['new'] = pd.Series([0 for x in range(len(df.index))])
df['recent_px'] = pd.Series([recent_price for x in range(len(df.index))])

df['intrinsic_value'] = (df['recent_px'] - df['strike'])
df['intrinsic_value'] = np.where(df['intrinsic_value'] < 0, 0, df['intrinsic_value'])
df['intrinsic_value'] = pd.Series([round(val, 2) for val in df['intrinsic_value']], index = df.index)
df['option_px'] = (df['bid'] + df['ask']) / 2
df['option_px'] = pd.Series([round(val, 2) for val in df['option_px']], index = df.index)
df['extrinsic_value'] = df['option_px'] - df['intrinsic_value']
df['extrinsic_value'] = np.where(df['extrinsic_value'] < 0, 0, df['extrinsic_value'])
#df['var2'] = pd.Series([round(val, 2) for val in df['var2']], index = df.index)
df['extrinsic_value'] = pd.Series([round(val, 2) for val in df['extrinsic_value']], index = df.index)
df['yield'] = df['extrinsic_value'] / df['recent_px']
#df['var3'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['var3']], index = df.index)
df['yield'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['yield']], index = df.index)
df['impliedVolatility'] = pd.Series([round(val, 2) for val in df['impliedVolatility']], index = df.index)
df['protection'] = df['option_px'] / df['recent_px']
df['protection'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['protection']], index = df.index)
dfobj = df[['recent_px','strike','option_px','extrinsic_value','yield','protection']]

dfobj.to_csv('yield1.csv')

