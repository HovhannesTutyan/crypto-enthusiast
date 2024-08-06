from BasicStats import mean, correlation, standard_deviation, de_mean
from sklearn.linear_model import LinearRegression
from collections import Counter, defaultdict
import math, random
import numpy as np
import json

# assuming we have alfa and betta, prediction will be
def predict(alfa, betta, x_i):
    return betta * x_i + alfa
# as we have in fact y_i, calculate the error
def error(alfa, betta, x_i, y_i):
    return y_i - predict(alfa, betta, x_i)
# the least square solution is to find alfa and betta, that have smallest sum of squared error
def sum_of_squared_errors(alfa, betta, x, y):
    return sum(error(alfa, betta, x_i, y_i) ** 2 for x_i, y_i in zip(x, y))
def least_squares_fit(x, y):
    """given the training values for x and y, find the least_squared values for alfa and betta"""
    betta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alfa = mean(y) - betta * mean(x)
    return alfa, betta
def total_sum_of_squares(y):
    """R - total squared variation of y_i's from their mean"""
    return sum(v ** 2 for v in de_mean(y))
def r_squared(alpha, beta, x, y):
    """R ** 2 the fraction of variation in y captured by the model, which equals
    1 - the fraction of variation in y not captured by the model"""
    return 1.0 - (sum_of_squared_errors(alpha, beta, x, y) / total_sum_of_squares(y))

with open('solana.json', 'r', encoding='utf8') as f:
    data = json.load(f)
price_usd_sol  = [entry["price_usd"] for entry in data if entry["symbol"] == "SOL"]
volume_24h_sol = [entry["volume_24h"] for entry in data if entry["symbol"] == "SOL" ]
market_cap_sol = [entry["market_cap"] for entry in data if entry["symbol"] == "SOL" ]
price_usd_btc  = [entry["price_usd"] for entry in data if entry["symbol"] == "BTC"]
volume_24h_btc = [entry["volume_24h"] for entry in data if entry["symbol"] == "BTC" ]
market_cap_btc = [entry["market_cap"] for entry in data if entry["symbol"] == "BTC" ]

alfa_sol, betta_sol = least_squares_fit(price_usd_sol, market_cap_sol)
alfa_btc, betta_btc = least_squares_fit(price_usd_btc, market_cap_btc)

print(f"The equity for Solana will be {alfa_sol} + n * {betta_sol}")
print(f"The equity for Bitcoin will be {alfa_btc} + n * {betta_btc}")

r_Squared = r_squared(alfa_sol, betta_sol, price_usd_sol, market_cap_sol)
print(f'R_2 will be {r_Squared}')

""" The equity for Solana will be -1472756295.9399872 + n * 458811442.2205495
    The equity for Bitcoin will be -10417770112.389526 + n * 19845560.495750498
    Our model tells, that if price is 0, market_up for solana will be -1472756295.9399872 and will rise with 458811442.2205495 for each 1 dollar up."""

# Verify model with scikit-learn 
def verify_with_sklearn(x, y):
    model = LinearRegression()
    x_reshaped = np.array(x).reshape(-1, 1)
    model.fit(x_reshaped, y)
    alpha = model.intercept_
    beta = model.coef_[0]
    r_squared = model.score(x_reshaped, y)
    return alpha, beta, r_squared

alpha_sol_sklearn, beta_sol_sklearn, r_squared_sol_sklearn = verify_with_sklearn(price_usd_sol, market_cap_sol)
alpha_btc_sklearn, beta_btc_sklearn, r_squared_btc_sklearn = verify_with_sklearn(volume_24h_btc, market_cap_btc)
print(r_squared_sol_sklearn)