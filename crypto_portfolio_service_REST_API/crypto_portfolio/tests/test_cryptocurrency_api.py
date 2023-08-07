"""
Tests for the cryptocurrency API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.models import User
from crypto_portfolio.models import Cryptocurrency


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


def get_list_of_crypto_selected_user_portfolio():
    """Return content of user cryptocurrency portfolio."""
    return User.objects.all()[0].crypto.all()


class NotAuthenticatedUserTests(TestCase):
    """Tests for not authenticated user."""

    def setUp(self):
        self.client = APIClient()

    def test_add_coin_not_authenticated_error(self):
        """Test return error if not authenticated user created coin."""
        payload = generate_payload()
        result = self.client.post(CREATE_COIN_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    """Tests for authenticated user."""

    def setUp(self):
        self.user = create_user(
            email='test_email@example.com',
            username='test_username',
            password='test_password',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_created_coin_successful(self):
        """Test coin created successful by authenticated user."""
        payload = generate_payload()
        result = self.client.post(CREATE_COIN_URL, payload)
        user_portfolio = get_list_of_crypto_selected_user_portfolio()

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_portfolio[0].name, payload['name'])
