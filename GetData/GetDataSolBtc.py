import os
import sys
import json
import django
import requests
from datetime import datetime
from django.utils import timezone
from collections import Counter, defaultdict

# Ensure the 'Root' folder is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'root')))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from main.models import Coin, HistoryData

# Constants
COINS = [
    {'id': 'solana', 'name': 'Solana', 'symbol': 'SOL'},
    {'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}
]
DAYS = 365
all_data = []
by_symbol = []
for coin_info in COINS:
    COIN_ID = coin_info["id"]
    API_URL = f'https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart'
    # Fetch historical data from CoinGecko
    response = requests.get(API_URL, params={'vs_currency': 'usd', 'days': DAYS})
    data = response.json()
    # Ensure Coin exists in database
    coin, created = Coin.objects.get_or_create(name=coin_info["name"], symbol=coin_info["symbol"])
    # Process and store historical data
    for i in range(len(data['market_caps'])):
        timestamp, market_cap = data['market_caps'][i]
        price_usd = data['prices'][i][1]
        volume_24h = data['total_volumes'][i][1]
        date = datetime.utcfromtimestamp(timestamp / 1000).date()
        data_point = {
            "name":coin_info["name"],
            "symbol":coin_info["symbol"],
            "date": date.isoformat(),
            "price_usd": price_usd,
            "market_cap": market_cap,
            "volume_24h": volume_24h
        }
        # Add the data point to the list
        by_symbol.append(data_point)
        # Avoid duplications
        if not HistoryData.objects.filter(coin=coin, date=date).exists():
            HistoryData.objects.create(
                coin=coin,
                date=date.isoformat(),
                market_cap=market_cap,
                price_usd=price_usd,
                volume_24h=volume_24h,
            )
    all_data.append({
        "coin": coin_info["name"],
        "data": by_symbol
    })
with open("solana.json", 'w') as json_file:
    json.dump(by_symbol, json_file, indent=4)


print('Historical market cap data for Solana has been updated.')
