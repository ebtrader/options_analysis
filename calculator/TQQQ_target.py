import yfinance as yf

tqqq_ticker = "TQQQ"

df_tqqq = yf.download(tickers=tqqq_ticker, interval='5m', period ='1d')
recent_tqqq = df_tqqq['Close'].iloc[-1]
print(df_tqqq['Close'])
print(recent_tqqq)

nq_ticker = 'NQ=F'
df_nq = yf.download(tickers=nq_ticker, interval='5m', period ='1d')
recent_nq = df_nq['Close'].iloc[-1]
print(df_nq['Close'])
print(recent_nq)


nq_current = recent_nq
tqqq_current = recent_tqqq
nq_target = 11500
tqqq_target = ((nq_target / nq_current - 1) * 3 + 1)* tqqq_current
print(tqqq_target)
