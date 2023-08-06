from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import CryptocurrencySerializer
from .models import Cryptocurrency
from user.models import User


class CryptocurrencyViewSet(viewsets.ModelViewSet):
    """View for cryptocurrency management."""
    serializer_class = CryptocurrencySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cryptocurrency.objects.filter(user=user)
        return queryset
