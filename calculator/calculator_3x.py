#NQ_start_price = 12651
NQ_start_price = float(input('what is the futures opening price?:   ')) #12475
TQQQ_start_price = float(input('what is the 3x ETF opening price?:   ')) #170
NQ_end_price = float(input('what is the futures target price?:   '))  #12640
#TQQQ_start_price = 172.41

NQ_pct_change = ((NQ_end_price / NQ_start_price) - 1)*3
TQQQ_end_price = TQQQ_start_price * (1 + NQ_pct_change)
#print ('%.2f'%TQQQ_end_price)
print ('3x ETF target price is %.2f'%TQQQ_end_price)
