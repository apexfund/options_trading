import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime 
from pandas_datareader import data as pdr

def monteCarloSlow(S, K, vol, r, N, M, market_value, T):
    dt = T/N
    nudt = (r - 0.5*vol**2)*dt
    volstd = vol*np.sqrt(dt)
    lnS = np.log(S) # natural log of s

    # standard error placeholders
    sum_CT = 0
    sum_CT2 = 0


    # Monte Carlo method
    # for simulation i in m simulations 
    # for j in the time steps N

    for i in range(M):
        lnSt = lnS
        for j in range(N):

            # calculate the next log of st variable
            # adding drift and voldstd with random variable 
            # variable is 0 with variance 1
            lnSt = lnSt + nudt + volstd*np.random.normal()


        ST = np.exp(lnSt)  # exponential of the final payoff 
        CT = max(0, ST - K) # max between stock price and strike price 
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT + CT * CT  # sum of the squares
    
    # compute expection and 
    C0 = np.exp(-r*T)*sum_CT/M
    sigma = np.sqrt((sum_CT - sum_CT* sum_CT/M) * np.exp(-2*r*T) / (M-1))
    SE = sigma/np.sqrt(M) # normalize by M which is the number of variables

    # simulating random variables and therefore the average of the result is random
    print("Call Value is &{0} with SE + / - {1}".format((np.round(C0,2), np.round(SE, 2))))

def monteCarloFast(S, K, vol, r, N, M, market_value, T):
    
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


# def monteCarlo(S, T, r, q, sigma, steps, N):

#     dt = T/steps
#     ST = np.log(S) + np.cumsum(((r - q - sigma ** 2/2) * dt) + sigma*np.sqrt(dt) * np.random.normal(size=(steps,N)), axis=0)
#     return np.exp(ST)


# stock_price = 100
# strike_price= 100
# time_to_maturity = 1/2
# risk_free_rate = 0.05
# annual_volatility = 0.25
# annual_dividend_rate = 0.02
# time_steps = 100
# trails = 100

# paths  = monteCarlo(stock_price, time_to_maturity, risk_free_rate, annual_dividend_rate, annual_volatility, time_steps, trails)
# plt.plot(paths)
# plt.xlabel("Time Increments")
# plt.ylabel("Stock Price")
# plt.title("Geometric Brownian Motion")
# plt.show()


S = 101.15
K = 98.01
Vol = 0.0991
r = 0.01
N = 10
M = 1000
market_value = 3.86
T = ((datetime.date(2022,9,30)-datetime.date.today()).days+1)/365    

#monteCarloSlow(S, K, Vol, r, N, M, market_value, T)
monteCarloFast(S, K, Vol, r, N, M, market_value, T)
