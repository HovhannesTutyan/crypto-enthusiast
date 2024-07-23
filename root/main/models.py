from django.db import models

class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.symbol}"

class HistoryData(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='history_data')
    date = models.DateField()
    price_usd = models.IntegerField()
    volume_24h = models.IntegerField()
    market_cap = models.IntegerField()

    class Meta:
        unique_together = ('coin', 'date')

    def __str__(self) -> str:
        return f"{self.coin.symbol} - {self.date}"