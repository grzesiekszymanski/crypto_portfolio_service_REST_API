from django.db import models
from django.conf import settings


class Cryptocurrency(models.Model):
    """This class represents simple cryptocurrency."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="crypto"
    )
    name = models.CharField(max_length=30)
    price = models.CharField(default=0)
    amount = models.CharField(default=0)
    worth = models.CharField(default=0)
    coin_profit_loss_percent_24h = models.CharField(default=0)
    coin_participation_in_portfolio = models.CharField(default=0)
    last_update = models.CharField(max_length=25, default="")

    def __str__(self):
        return self.name


class PortfolioData(models.Model):
    """This class represents general data related with user portfolio."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="general_data"
    )
    total_value = models.CharField(default=0)
    total_profit_loss = models.CharField(default=0)
    total_profit_loss_percent = models.CharField(default=0)
    total_profit_loss_24h = models.CharField(default=0)
    total_profit_loss_percent_24h = models.CharField(default=0)

    def __str__(self):
        return f"{self.user}'s portfolio"
