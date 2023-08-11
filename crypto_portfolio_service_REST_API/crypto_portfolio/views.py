from pycoingecko import CoinGeckoAPI

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CryptocurrencySerializer,
    PortfolioDataSerializer,
    AvailableCoinsSerializer
)

from .models import Cryptocurrency, PortfolioData
from user.models import User


cg = CoinGeckoAPI()


def retrieve_coins_to_delete(coins_to_retrieve) -> list:
    """Get input and return list of coin names to delete."""
    splitted_coins = coins_to_retrieve[1:].split(', ')
    return [coin_name.split(': ')[1].split('>')[0] for coin_name in splitted_coins]


class CryptocurrencyViewSet(viewsets.ModelViewSet):
    """View for cryptocurrency management."""

    serializer_class = CryptocurrencySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cryptocurrency.objects.filter(user=user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        # Remove selected coin if exist in authenticated user portfolio.
        try:
            names_to_delete = retrieve_coins_to_delete(kwargs['pk'])
            for coin in user.crypto.all():
                if coin.name in names_to_delete:
                    deleted_coin = coin.name
                    coin.delete()
                    print(f'[INFO] --- Removed following coin: {deleted_coin} ---')

            return Response(status=status.HTTP_204_NO_CONTENT)
        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PortfolioDataViewSet(viewsets.ModelViewSet):
    """View for portfolio data management."""

    serializer_class = PortfolioDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = PortfolioData.objects.filter(user=user)
        return queryset


class AvailableCoinsView(APIView):
    """View for all available coins via external API."""

    def get(self, request, format=None):
        available_coins = [coin['name'] for coin in cg.get_coins_list()]
        serializer = AvailableCoinsSerializer({'available_coins': available_coins})

        return Response(serializer.data, status=status.HTTP_200_OK)
