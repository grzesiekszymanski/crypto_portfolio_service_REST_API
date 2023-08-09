"""
Tests for the cryptocurrency API.
"""
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.models import User


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


def read_current_date_and_time():
    """Return current date and time."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class NotAuthenticatedUserTests(TestCase):
    """Tests for not authenticated user."""

    def setUp(self):
        self.client = APIClient()

    def test_add_coin_not_authenticated_error(self):
        print(f"Started {'test_add_coin_not_authenticated_error'}")
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
        print(f"Started {'test_created_coin_successful'}")
        """Test coin created successful by authenticated user."""
        payload = generate_payload('bitcoin', 3.0)
        result = self.client.post(CREATE_COIN_URL, payload)
        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_portfolio[0].name, payload["name"])

    def test_created_coin_visible_only_for_author(self):
        print(f"Started {'test_created_coin_visible_only_for_author'}")
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
        print(f"Started {'test_coin_duplication_not_possible'}")
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
        print(f"Started {'test_created_multiple_coins_successful'}")
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

    def test_formatting_coin_name(self):
        print(f"Started {'test_formatting_coin_name'}")
        """Test size of letters or whitespaces do not have impact for searching coin."""
        coin_name_variants = [
            'bitcoin',
            'BITCOIN',
            'BiTcOiN',
            'BITcoin',
            ' bitcoin',
            'BITCOIN '
        ]
        results = []

        for coin_name in coin_name_variants:
            payload = generate_payload(coin_name, 1)
            results.append(self.client.post(CREATE_COIN_URL, payload))

        for result in results:
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_added_coin_with_amount_0(self):
        print(f"Started {'test_added_coin_with_amount_0'}")
        """Test coin was added correctly after creation with amount 0."""
        payload = generate_payload('bitcoin', 0)
        result = self.client.post(CREATE_COIN_URL, payload)
        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(user_portfolio[0].amount), 0)

    def test_correctness_of_date_and_time(self):
        print(f"Started {'test_correctness_of_date_and_time'}")
        """Test date and time were added correctly."""
        payload = generate_payload('bitcoin', 2)
        result = self.client.post(CREATE_COIN_URL, payload)
        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)
        current_date_and_time = read_current_date_and_time()

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_portfolio[0].date, current_date_and_time)

    def test_remove_selected_coin_from_portfolio(self):
        print(f"Started {'test_remove_selected_coin_from_portfolio'}")
        """Remove selected coin from authenticated user portfolio."""
        payload = generate_payload('bitcoin', 2)
        result = self.client.post(CREATE_COIN_URL, payload)

        user_portfolio = get_list_of_crypto_selected_user_portfolio(user_index=0)
        num_coins_before_del = len(user_portfolio.all())

        response = self.client.delete(f'{CREATE_COIN_URL}{user_portfolio}/')
        num_coins_after_del = len(user_portfolio.all())

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(num_coins_before_del, 1)
        self.assertEqual(num_coins_after_del, 0)

    def test_reset_portfolio(self):
        print(f"Started {'test_reset_portfolio'}")
        """Test portfolio reset works correctly."""
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

        portfolio_len_before_reset = len(user_portfolio.all())
        response = self.client.delete(f'{CREATE_COIN_URL}{user_portfolio}/')
        portfolio_len_after_reset = len(user_portfolio.all())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(portfolio_len_before_reset, len(coins_to_create))
        self.assertEqual(portfolio_len_after_reset, 0)

    def test_incorrect_coin_name_delete_error(self):
        print(f"Started {'test_incorrect_coin_name_error'}")
        """Test sending incorrect coin name to delete returns bad request status."""
        payload = generate_payload('bitcoin', 2)
        result = self.client.post(CREATE_COIN_URL, payload)
        response = self.client.delete(f'{CREATE_COIN_URL}incorrect_name/')

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_coin_name_create_error(self):
        print(f"Started {'test_incorrect_coin_name_create_error'}")
        """Test sending incorrect coin name to create returns bad request status."""
        payload = generate_payload('b_i_t_c_o_i_n', 2)
        with self.assertRaises(Exception):
            self.client.post(CREATE_COIN_URL, payload)

    def test_incorrect_coin_amount_create_error(self):
        print(f"Started {'test_incorrect_coin_amount_create_error'}")
        """Test sending incorrect coin amount to create returns bad request status."""
        payload = generate_payload('bitcoin', -2)
        with self.assertRaises(Exception):
            self.client.post(CREATE_COIN_URL, payload)
