import math
import numpy as np
import pandas as pd
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

def monteCarlo(S, K, vol, r, N, M, market_value, T):
    
    # Precompute constants
    dt = T/N
    nudt = (r - 0.5*vol**2)*dt
    volstd = vol * np.sqrt(dt)
    lnS = np.log(S)

    # Monte Carlo Method
    Z = np.random.normal(size=(N, M)) # matrix Z of size time steps by number of simulations
    
    # represent the small increments we are moving in time 
    delta_lnSt = nudt + volstd * Z    # new matrix which is the delta of the process and is drift term + vol  
    lnSt = lnS + np.cumsum(delta_lnSt, axis=0) # get cumulative sums of the deltas
    
    # concatenate numpy array of shape 1 by the number of simulations with the fill value which is the natural log of st
    # this is for completeness
    lnSt = np.concatenate((np.full(shape=(1,M), fill_value=lnS), lnSt))

    # Compute expectation and SE
    ST = np.exp(lnSt)
    CT = np.maximum(0, ST-K)
    C0 = np.exp(-r*T)*np.sum(CT[-1])/M # take the final column, take its sum, and get the discounted payoff of the average

    sigma = np.sqrt(np.sum((CT[-1]-C0)**2) / (M-1))
    SE = sigma/np.sqrt(M)

    print("Call value is ${0} with SE +/- {1}".format(np.round(C0,2), np.round(SE, 2)))

    x1 = np.linspace(C0-3*SE, C0-1*SE, 100)
    x2 = np.linspace(C0-1*SE, C0+1*SE, 100)
    x3 = np.linspace(C0+1*SE, C0+3*SE, 100)
    s1 = stats.norm.pdf(x1, C0, SE)
    s2 = stats.norm.pdf(x2, C0, SE)
    s3 = stats.norm.pdf(x3, C0, SE)
    plt.fill_between(x1, s1, color='tab:blue',label='> StDev')
    plt.fill_between(x2, s2, color='cornflowerblue',label='1 StDev')
    plt.fill_between(x3, s3, color='tab:blue')
    plt.plot([C0,C0],[0, max(s2)*1.1], 'k',
            label='Theoretical Value')
    plt.plot([market_value,market_value],[0, max(s2)*1.1], 'r',
            label='Market Value')
    plt.ylabel("Probability")
    plt.xlabel("Option Price")
    plt.legend()
    plt.show()

# Option Metrics

S = 138.34  # stock price
K = 135 # strike price
vol = 0.5154 # implied volatility
r = 0.01 # risk free return rate
N = 10 # number of time steps
M = 1000 # number of simulations
market_value = 7.77 # market price for option
T = ((datetime.date(2022,10,28)-datetime.date.today()).days+1)/365 # Time calculation from now to option expiration




monteCarlo(S, K, vol, r, N, M, market_value, T)

