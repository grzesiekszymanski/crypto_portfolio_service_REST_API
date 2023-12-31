"""
URL mappings for the crypto portfolio API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("manage", views.CryptocurrencyViewSet, basename="manage")

app_name = "crypto_portfolio"

urlpatterns = [
    path("", include(router.urls)),
    path("available_coins", views.AvailableCoinsView.as_view(), name="available_coins"),
]
