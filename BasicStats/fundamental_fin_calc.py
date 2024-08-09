import yfinance as yf
import numpy as np
import pandas as pd
import pyfolio as pf
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

RISKY_ASSETS = ['SOL-USD', 'DOT-USD']
START_DATE = '2023-01-10'
END_DATE = '2023-01-20'

# download stock prices from Yahoo finance
prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, auto_adjust=True)

# define main functions for estimation
def daily_perc_change(data):
    df = pd.DataFrame(data)
    changes = ((df['Close'] / df['Close'].shift(1)) - 1) * 100
    return changes.dropna()

def daily_cumulative_change(perc_change):
    changes_cumulative = (1 + perc_change / 100).cumprod()
    return changes_cumulative

# daily percentage change to the previous day
returns  = daily_perc_change(prices_df)

# $1 invested in the first day return on current day
cumulative_returns = daily_cumulative_change(returns)
cumulative_returns.plot(figsize=(12,8))
plt.legend(loc=2)
plt.show()