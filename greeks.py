from scipy.stats import norm
from math import *

#http://janroman.dhis.org/stud/I2014/BS2/BS_Daniel.pdf

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

def Black_Scholes_Greeks_Call(S, K, r, v, T, d):
    T_sqrt = sqrt(T)
    d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*T_sqrt)
    d2 = d1-v*T_sqrt
    Delta = norm.cdf(d1)
    Gamma = norm.pdf(d1)/(S*v*T_sqrt)
    Theta =- (S*v*norm.pdf(d1))/(2*T_sqrt) - r*K*exp( -r*T)*norm.cdf(d2)
    Vega = S * T_sqrt*norm.pdf(d1)
    Rho = K*T*exp(-r*T)*norm.cdf(d2)
    return Delta, Gamma, Theta, Vega, Rho

#print (Black_Scholes_Greeks_Call(100, 100, 0.005, 0.06, 0.4, 0))
print(Black_Scholes_Greeks_Call(167.59, 167.5, 0, .60, 0.019, 0))

"""Calculating the partial derivatives for a Black Scholes Option (Put)
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

def Black_Scholes_Greeks_Put(S, K, r, v, T, d):
    T_sqrt = sqrt(T)
    d1 = (log(float(S)/K)+r*T)/(v*T_sqrt) + 0.5*v*T_sqrt
    d2 = d1-(v*T_sqrt)
    Delta = -norm.cdf(-d1)
    Gamma = norm.pdf(d1)/(S*v*T_sqrt)
    Theta = -(S*v*norm.pdf(d1)) / (2*T_sqrt)+ r*K * exp(-r*T) * norm.cdf(-d2)
    Vega = S * T_sqrt * norm.pdf(d1)
    Rho = -K*T*exp(-r*T) * norm.cdf(-d2)
    return Delta, Gamma, Theta, Vega, Rho

#print (Black_Scholes_Greeks_Put(100, 100, 0.005, 0.06, 0.4, 0))

def BlackScholes(CallPutFlag, S, K, r, v, T, d):
    d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*sqrt(T))
    d2 = d1-v*sqrt(T)
    if CallPutFlag=='c':
        return S*exp(-d*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
    else:
        return K*exp(-r*T)*norm.cdf(-d2)-S*exp(-d*T)*norm.cdf(-d1)

#print(BlackScholes('c', 100, 100, .005, 0.06, 0.4, 0))
print(BlackScholes('c', 167.59, 161, 0.0001, .60, 0.019, 0)) # divide 5 days by 252