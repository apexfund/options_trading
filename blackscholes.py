#IMPORTS
import numpy as np
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho

#VARIABLES
r = 0.01
S = 30
K = 40
T = 240/365
sigma = 0.30

#BLACKSCHOLES
def blackScholes(r, S, K, T, sigma, type="C"):
    "Calculate black scholes option price for a call or put."
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            price = S * norm.cdf(d1, 0, 1) - K*np.exp(-r*T) * norm.cdf(d2, 0, 1)
        elif type == "P":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0 ,1) - S*norm.cdf(-d1, 0, 1)

        return price
    except:
        print("Please confirm all option parameters above!")

#DELTA
def delta_calc(r, S, K, T, sigma, type="C"):
    "Calculate delta of an option."
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    try:
        if type == "C":
            delta_calc = norm.cdf(d1, 0, 1)
        elif type == "P":
            delta_calc = -norm.cdf(-d1, 0, 1)

        return delta_calc
    except:
        print("Please confirm all option parameters above!")

#GAMMA
def gamma_calc(r, S, K, T, sigma, type="C"):
    "Calculate gamma of an option."
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:

        gamma_calc = norm.pdf(d1, 0, 1)/(S*sigma*np.sqrt(T))
        return gamma_calc
    except:
        print("Please confirm all option parameters above!")

#VEGA
def vega_calc(r, S, K, T, sigma, type="C"):
    "Calculate vega of an option."
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        
        vega_calc = S*norm.pdf(d1,0,1) * np.sqrt(T)
        return vega_calc * 0.01
    
    except:
        print("Please confirm all option parameters above!")

#THETA
def theta_calc(r, S, K, T, sigma, type="C"):
    "Calculate theta of an option."
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            theta_calc = -S * norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T) * norm.cdf(d2, 0, 1)
        elif type == "P":
            theta_calc = -S * norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T) * norm.cdf(-d2, 0, 1)

        return theta_calc / 365  
    except:
        print("Please confirm all option parameters above!")

#RHO
def rho_calc(r, S, K, T, sigma, type="C"):
    "Calculate rho of an option." 
    d1 = (np.log(S/K) + (r + (sigma**2)/2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            rho_calc = K*T*np.exp(-r*T) * norm.cdf(d2, 0, 1)
        elif type == "P":
            rho_calc = -K*T*np.exp(-r*T) * norm.cdf(-d2, 0, 1)

        return rho_calc * 0.01
    except:
        print("Please confirm all option parameters above!")

#OUTPUTS
print("Option price is: ", blackScholes(r, S, K, T, sigma))
print("Delta price is: ",  delta_calc(r, S, K, T, sigma))
print("Gamma price is: ",  gamma_calc(r, S, K, T, sigma))
print("Vega price is: ",  vega_calc(r, S, K, T, sigma))
print("Theta price is: ", theta_calc(r, S, K, T, sigma))
print("Rho price is: ", theta_calc(r, S, K, T, sigma))