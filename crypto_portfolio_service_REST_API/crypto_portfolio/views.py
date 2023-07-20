from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import CryptocurrencySerializer
from .models import Cryptocurrency


class CryptocurrencyViewSet(viewsets.ModelViewSet):
    """View for cryptocurrency management."""

    serializer_class = CryptocurrencySerializer
    queryset = Cryptocurrency.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
