import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from math import *
from scipy.stats import norm

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

opt = ticker.option_chain('2020-12-24')
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
df['recent_px'] = recent_price

df['intrinsic_value'] = (df['recent_px'] - df['strike'])
df['intrinsic_value'] = np.where(df['intrinsic_value'] < 0, 0, df['intrinsic_value'])
#df['intrinsic_value'] = pd.Series([round(val, 2) for val in df['intrinsic_value']], index = df.index)
df['option_px'] = (df['bid'] + df['ask']) / 2
#df['option_px'] = pd.Series([round(val, 2) for val in df['option_px']], index = df.index)
df['extrinsic_value'] = df['option_px'] - df['intrinsic_value']
df['extrinsic_value'] = np.where(df['extrinsic_value'] < 0, 0, df['extrinsic_value'])
#df['var2'] = pd.Series([round(val, 2) for val in df['var2']], index = df.index)
#df['extrinsic_value'] = pd.Series([round(val, 2) for val in df['extrinsic_value']], index = df.index)
df['yield'] = df['extrinsic_value'] / df['recent_px']
#df['var3'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['var3']], index = df.index)
#df['yield'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['yield']], index = df.index)
#df['impliedVolatility'] = pd.Series([round(val, 2) for val in df['impliedVolatility']], index = df.index)
df['protection'] = df['option_px'] / df['recent_px']
#df['protection'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['protection']], index = df.index)

#greeks

"""Calculating the partial derivatives for a Black Scholes Option (Call)
# S - Stock price
# K - Strike price
# T - Time to maturity
# r - Riskfree interest rate
# d - Dividend yield
# v - Volatility
Return:
Delta: partial wrt S
Gamma: second partial wrt S
Theta: partial wrt T
Vega: partial wrt v
Rho: partial wrt r """


""" def Black_Scholes_Greeks_Call(S, K, r, v, T, d):
    T_sqrt = sqrt(T)
    d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*T_sqrt)
    d2 = d1-v*T_sqrt
    Delta = norm.cdf(d1)
    Gamma = norm.pdf(d1)/(S*v*T_sqrt)
    Theta =- (S*v*norm.pdf(d1))/(2*T_sqrt) - r*K*exp( -r*T)*norm.cdf(d2)
    Vega = S * T_sqrt*norm.pdf(d1)
    Rho = K*T*exp(-r*T)*norm.cdf(d2)
    return Delta, Gamma, Theta, Vega, Rho

print(Black_Scholes_Greeks_Call(167.59, 167.5, 0, .60, 0.019, 0)) 0.519 use 252 as base for days to expiration"""



df['S'] = df['recent_px']
df['K'] = df['strike']
expiration_date = str(df['contractSymbol'].iloc[0])
#print(expiration_date)
exp_slice = expiration_date[6:10] + expiration_date[4:6]
#print(exp_slice)
today = datetime.today()
#print(today)

def __datetime(date_str):
    return datetime.strptime(date_str, '%m%d%y')

end = __datetime(exp_slice)
#print(end)

days_to_expiration = end - today
#print(days_to_expiration)
days_left = days_to_expiration.days
#print(days_left)
black_scholes_days_left = days_left / 252
#print(black_scholes_days_left)
df['T'] = black_scholes_days_left
risk_free_rate = .005
df['r'] = risk_free_rate
df['v'] = df['impliedVolatility']
dividend_rate = 0
df['d'] = dividend_rate


df['T_sqrt'] = np.sqrt(df['T'])
#d1 = (log(float(S) / K) + ((r - d) + v * v / 2.) * T) / (v * T_sqrt)

df['d1'] = (np.log(df['S'].astype(float) / df['K']) + (( df['r'] - df['d'] ) + df['v'] * df['v'] / 2)  * df['T'] )  / (df['v'] * df['T_sqrt'])
#Delta = norm.cdf(d1)
df['delta_calc'] = norm.cdf(df['d1'])
df.to_csv('complete.csv')

dfobj = df[['recent_px','strike','option_px','extrinsic_value','yield','protection', 'delta_calc']]

dfobj.to_csv('delta.csv')