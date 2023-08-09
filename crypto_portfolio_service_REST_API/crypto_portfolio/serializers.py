"""
Serializers for cryptocurrency portfolio.
"""
from datetime import datetime
from pycoingecko import CoinGeckoAPI

from rest_framework import serializers

from .models import Cryptocurrency
from user.models import User


class CryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for cryptocurrency."""

    class Meta:
        model = Cryptocurrency
        fields = [
            "name",
            "price",
            "amount",
            "worth",
            "total_profit_loss",
            "total_profit_loss_percent",
            "profit_loss_24h",
            "profit_loss_percent_24h",
            "participation_in_portfolio",
            "date",
        ]

    cg = CoinGeckoAPI()

    def _get_coin_price(self, coin_name):
        """Get coin name and return it's current price in USD."""
        current_coin_price = self.cg.get_price(
            ids=coin_name.lower(), vs_currencies="usd"
        )
        price_in_usd = current_coin_price[f"{coin_name.lower()}"]["usd"]

        return price_in_usd

    @staticmethod
    def _calculate_worth_of_added_coin(coin_price_usd, amount):
        """Calculate current worth of added cryptocurrency in USD."""
        return coin_price_usd * amount

    @staticmethod
    def _get_coin_names_from_portfolio(user):
        """Return coin list of already existing coins in selected user portfolio."""
        return [coin.name for coin in user.crypto.all()]

    @staticmethod
    def _calculate_average_price(
        average_price_before, current_price, coin_amount_before, coin_amount_to_add
    ):
        """Return average price for coin if user added it before."""
        return round(
            (
                coin_amount_before * average_price_before
                + coin_amount_to_add * current_price
            ),
            2,
        ) / (coin_amount_before + coin_amount_to_add)

    def _get_coin_for_update(self, user, coin_name):
        """Get and return selected coin for update from user portfolio."""
        available_coins = self._get_coin_names_from_portfolio(user)
        index = available_coins.index(coin_name)
        return user.crypto.all()[index]

    @staticmethod
    def _read_current_date_and_time():
        """Return current date and time."""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def create(self, validated_data):
        """Create cryptocurrency in authenticated user portfolio."""
        # Get and calculate cryptocurrency parameters.
        user = self.context["request"].user
        coin_name = validated_data["name"]
        coin_amount = validated_data["amount"]
        portfolio_coins = self._get_coin_names_from_portfolio(user)

        # Calculate coin properties.
        coin_price_usd = self._get_coin_price(coin_name)
        worth = self._calculate_worth_of_added_coin(
            coin_price_usd, validated_data["amount"]
        )

        # Set cryptocurrency parameters.
        if coin_name in portfolio_coins:
            coin_for_update = self._get_coin_for_update(user, coin_name)
            coin_for_update.price = self._calculate_average_price(
                float(coin_for_update.price),
                float(coin_price_usd),
                float(coin_for_update.amount),
                float(coin_amount),
            )

            coin_for_update.amount = float(coin_for_update.amount) + float(coin_amount)
            coin_for_update.worth = float(coin_for_update.worth) + float(worth)
            coin_for_update.date = self._read_current_date_and_time()

            coin_for_update.save()
        else:
            validated_data["price"] = coin_price_usd
            validated_data["worth"] = worth
            user.crypto.create(**validated_data)

        return Cryptocurrency
