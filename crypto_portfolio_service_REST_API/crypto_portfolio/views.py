from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CryptocurrencySerializer

from .models import Cryptocurrency
from user.models import User


def get_available_coins_and_ids(user):
    """Return coin list of already existing coins, and it's id's in selected user portfolio."""
    return {coin.id: coin.name for coin in user.crypto.all()}


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
        available_coins_and_ids = get_available_coins_and_ids(user)

        id_to_delete = int(kwargs['pk'])
        name_to_delete = available_coins_and_ids[int(kwargs['pk'])]

        # Remove selected coin if exist in authenticated user portfolio.
        if name_to_delete != '' and name_to_delete != 'all':
            for coin in user.crypto.all():
                if coin.pk == id_to_delete:
                    coin.delete()
                    print(f'[INFO] --- Removed following coin: {name_to_delete} ---')

                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # # Remove all coins from authenticated user portfolio.
        # elif to_delete.lower() == 'all':
        #     if len(available_coins) == 0:
        #         pass
        #         # TODO: Add error handling here.
        #     else:
        #         user.crypto.all().delete()
        #         print('[INFO] --- Portfolio cleaned ---')
        #
        # # Incorrect input.
        # else:
        #     pass
        #     # TODO: Add error handling here.
