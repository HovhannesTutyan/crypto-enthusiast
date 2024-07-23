from django.contrib import admin
from .models import Coin, HistoryData

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

@admin.register(HistoryData)
class HistoryDataAdmin(admin.ModelAdmin):
    list_display = ('coin', 'date', 'price_usd', 'volume_24h', 'market_cap')
    list_filter = ('coin', 'date')
    search_fields = ('coin__name', 'coin__symbol')
