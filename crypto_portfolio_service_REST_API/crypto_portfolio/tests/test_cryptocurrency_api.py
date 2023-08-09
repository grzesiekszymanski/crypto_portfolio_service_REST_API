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


CREATE_COIN_URL = reverse("crypto_portfolio:manage-list")


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


def generate_payload(coin_name: str, amount: float) -> dict:
    payload = {
        "name": coin_name,
        "price": "",
        "amount": amount,
        "worth": "",
        "total_profit_loss": "",
        "total_profit_loss_percent": "",
        "profit_loss_24h": "",
        "profit_loss_percent_24h": "",
        "participation_in_portfolio": "",
        "date": "",
    }
    return payload


def get_list_of_crypto_selected_user_portfolio(user_index):
    """Return content of user cryptocurrency portfolio."""
    return User.objects.all()[user_index].crypto.all()


class NotAuthenticatedUserTests(TestCase):
    """Tests for not authenticated user."""

    def setUp(self):
        self.client = APIClient()

    def test_add_coin_not_authenticated_error(self):
        """Test return error if not authenticated user created coin."""
        payload = generate_payload('bitcoin', 3.0)
        result = self.client.post(CREATE_COIN_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    """Tests for authenticated user."""

    def setUp(self):
        self.user = create_user(
            email="test_email@example.com",
            username="test_username",
            password="test_password",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_created_coin_successful(self):
        """Test coin created successful by authenticated user."""
        payload = generate_payload('bitcoin', 3.0)
        result = self.client.post(CREATE_COIN_URL, payload)
        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_portfolio[0].name, payload["name"])

    def test_created_coin_visible_only_for_author(self):
        """Test created coin in portfolio is not visible for other users."""
        payload = generate_payload('bitcoin', 3.0)
        result = self.client.post(CREATE_COIN_URL, payload)

        # Create and force second user authentication.
        user2 = create_user(
            email="test_email2@example.com",
            username="test_username2",
            password="test_password2",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user2)

        user1_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)
        user2_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=1)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(user1_portfolio), 1)
        self.assertEqual(len(user2_portfolio), 0)

    def test_coin_duplication_not_possible(self):
        """Test it is not possible to duplicate cryptocurrency in portfolio."""
        payload = generate_payload('bitcoin', 3.0)
        result = self.client.post(CREATE_COIN_URL, payload)
        result2 = self.client.post(CREATE_COIN_URL, payload)

        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)
        total_amount = str(float(payload["amount"] + payload["amount"]))

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(user_portfolio), 1)
        self.assertEqual(total_amount, user_portfolio[0].amount)

    def test_created_multiple_coins_successful(self):
        """Test coins created successful by authenticated user."""
        coins_to_create = {
            'bitcoin': 3.0,
            'ethereum': 5.0,
            'cardano': 40.0
        }
        results = []

        for coin, amount in coins_to_create.items():
            payload = generate_payload(coin, amount)
            results.append(self.client.post(CREATE_COIN_URL, payload))

        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)

        for result in results:
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(user_portfolio.all()), len(results))
