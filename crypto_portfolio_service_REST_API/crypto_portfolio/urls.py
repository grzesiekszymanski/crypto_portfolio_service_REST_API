"""
URL mappings for the crypto portfolio API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("manage", views.CryptocurrencyViewSet)

app_name = "crypto_portfolio"

urlpatterns = [
    path("", include(router.urls)),
]
