"""
Serializers for cryptocurrency portfolio.
"""
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
            "date"
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

    def create(self, validated_data):
        """Create cryptocurrency in authenticated user portfolio."""
        # Get and calculate cryptocurrency parameters.
        user = self.context['request'].user
        coin_name = validated_data['name']
        coin_price_usd = self._get_coin_price(coin_name)
        worth = self._calculate_worth_of_added_coin(coin_price_usd, validated_data['amount'])

        # Set cryptocurrency parameters.
        validated_data['price'] = coin_price_usd
        validated_data['worth'] = worth

        user.crypto.create(**validated_data)
