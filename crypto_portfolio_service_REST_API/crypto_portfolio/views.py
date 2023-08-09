from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CryptocurrencySerializer

from .models import Cryptocurrency
from user.models import User


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
        names_to_delete = retrieve_coins_to_delete(kwargs['pk'])

        # Remove selected coin if exist in authenticated user portfolio.
        if len(names_to_delete) != 0:
            for coin in user.crypto.all():
                if coin.name in names_to_delete:
                    deleted_coin = coin.name
                    coin.delete()
                    print(f'[INFO] --- Removed following coin: {deleted_coin} ---')

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
