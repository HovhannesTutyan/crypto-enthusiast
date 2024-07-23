from django.shortcuts import render

from .models import Coin, HistoryData

solana = Coin.objects.get(symbol='SOL')
historical_data = HistoryData.objects.filter(coin=solana)
print(historical_data)
for data in historical_data:
    print(data.date, data.market_cap, data.price_usd, data.volume_24h)
