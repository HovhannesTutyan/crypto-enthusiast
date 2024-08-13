import yfinance as yf
import numpy as np
import pandas as pd
import pyfolio as pf
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

RISKY_ASSETS = ['SOL-USD']
START_DATE = '2023-01-10'
END_DATE = '2023-01-20'
WEIGHTS = np.array([2,3])
# WEIGHTS = np.array([0.1,0.2,0.3,0.4])

# download stock prices from Yahoo finance
prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, auto_adjust=True)
close_price = prices_df['Close']

wl = len(WEIGHTS)
pl = len(close_price)

# Function to calculate WMA
def calculate_wma(price, weights):
    wma = []
    if sum(weights) == 1:
    # Loop through weeks where WMA can be calculated
        for i in range(wl, pl):
            weighted_sum = np.dot(weights, price[i-wl:i])  # Apply weights
            wma.append(weighted_sum)
        return wma
    else:
        for i in range(wl, pl):
            weighted_sum = np.dot(weights, price[i-wl:i]) / sum(weights)  # Apply weights
            wma.append(weighted_sum)
        return wma
    
# calculate WMA for weeks 3 to 10
wma_results = calculate_wma(close_price, WEIGHTS)
absolute_errors = [abs(actual - forecast) for actual, forecast in zip(close_price[wl:pl], wma_results)]
mean_absolute_deviation = np.mean(absolute_errors)

# pring results
for i, (wma, error) in enumerate(zip(wma_results, absolute_errors), start=wl+1):
    print(f"Week {i}: WMA = {wma:.2f}, Absolute Error = {error:.2f}")
print("Mean Absolute Deviation", mean_absolute_deviation)
"""mean absolute deviation for weights = np.array([2,3]) is smaller than for weights = np.array([0.1,0.2,0.3,0.4]), 
which indicates that these weights smoothen the line better."""