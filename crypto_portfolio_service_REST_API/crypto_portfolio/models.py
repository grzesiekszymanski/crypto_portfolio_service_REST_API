from datetime import datetime

from django.db import models
from django.conf import settings


# current_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Cryptocurrency(models.Model):
    """This class represents simple cryptocurrency."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crypto'
    )
    name = models.CharField(max_length=30)
    price = models.CharField(default=0)
    amount = models.CharField(default=0)
    worth = models.CharField(default=0)
    total_profit_loss = models.CharField(default=0)
    total_profit_loss_percent = models.CharField(default=0)
    profit_loss_24h = models.CharField(default=0)
    profit_loss_percent_24h = models.CharField(default=0)
    participation_in_portfolio = models.CharField(default=0)
    date = models.CharField(max_length=25, default='')

    def __str__(self):
        return self.name
