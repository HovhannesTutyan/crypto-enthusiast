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

# download stock prices from Yahoo finance
prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, auto_adjust=True)
close_price = prices_df['Close']

""" In fact, people who find it difficult to draw trendlines often will substitute them for MOVING AVARAGES.
In general, though, if the price is above a particular moving average, then it can be said that the trend 
for that stock is up relative to that average and when the price is below a particular moving average, the trend is down."""

def moving_average(data, window_size=3):
    moving_averages = []
    for i in range(len(data) - window_size):
        window_average = np.mean(data[i : i + window_size])
        moving_averages.append(window_average)
    return moving_averages


print(f"Price for SOL-USD pair: {close_price}")
mov_avgs = moving_average(close_price)                                          # F_2 = (16.19 + 16.35 + 16.61) / 3 = 16.39; F_3 = (16.35 + 16.61 + 18.28) / 3 = 17.08 and so on
forecast_errors = [close_price[i+3] - ma for i, ma in enumerate(mov_avgs)]      # Actual - Forecast, F_3 = 18.28 - 16.39 = 1.89; F_4 = 24.24 - 17.08 = 7.16
absolte_errors = np.abs(forecast_errors)                                        # |forecast_errors|
mean_absolute_deviation = np.mean(absolte_errors)                               # Mean of absolute errors (1.89+7.16+3.15+1.77+0.68+2.26+1.01)/ 7 = 2.56
squared_errors = np.square(forecast_errors)                                     # Square for forecast errors
mean_squared_error = np.mean(squared_errors)                                    # Mean of squared errors

# Print the results
for i, ma in enumerate(mov_avgs, start=4):
    print(f"F_{i} = {ma:.2f}")
print ("Forecast errors", forecast_errors)
print( "Mean Absolute Deviation ", mean_absolute_deviation)
