"""
Tests for the cryptocurrency API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_COIN_URL = reverse('crypto_portfolio:manage-list')


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


def generate_payload():
    payload = {
        'name': 'bitcoin',
        'price': '',
        'amount': 3,
        'worth': '',
        'total_profit_loss': '',
        'total_profit_loss_percent': '',
        'profit_loss_24h': '',
        'profit_loss_percent_24h': '',
        'participation_in_portfolio': '',
        'date': ''
    }
    return payload


class NotAuthenticatedUserTests(TestCase):
    """Tests for not authenticated user."""

    def setUp(self):
        self.client = APIClient()

    def test_add_coin_not_authenticated_error(self):
        """Test return error if not authenticated user created coin."""
        payload = generate_payload()
        result = self.client.post(CREATE_COIN_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
