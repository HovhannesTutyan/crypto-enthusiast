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
COIN_ID = 'solana'
API_URL = f'https://api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart'
DAYS = 365
# Fetch historical data from CoinGecko
response = requests.get(API_URL, params={'vs_currency': 'usd', 'days': DAYS})
data = response.json()

# Ensure Coin exists in database
solana, created = Coin.objects.get_or_create(name='Solana', symbol='SOL')

by_symbol = []
# # Process and store historical data
for i in range(len(data['market_caps'])):
    timestamp, market_cap = data['market_caps'][i]
    price_usd = data['prices'][i][1]
    volume_24h = data['total_volumes'][i][1]
    date = datetime.utcfromtimestamp(timestamp / 1000).date()
    data_point = {
        "date": date.isoformat(),
        "price_usd": price_usd,
        "market_cap": market_cap,
        "volume_24h": volume_24h
    }

    # Add the data point to the list
    by_symbol.append(data_point)
    # Avoid duplications
    if not HistoryData.objects.filter(coin=solana, date=date).exists():
        HistoryData.objects.create(
            coin=solana,
            date=date.isoformat(),
            market_cap=market_cap,
            price_usd=price_usd,
            volume_24h=volume_24h,
        )

with open("solana.json", 'w') as json_file:
    json.dump(by_symbol, json_file, indent=4)


print('Historical market cap data for Solana has been updated.')
