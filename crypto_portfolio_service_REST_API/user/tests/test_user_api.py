"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
PAYLOAD = {
    "email": "test_email@example.com",
    "username": "test_username",
    "password": "test_password",
}


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test for the public features of the user API."""

    def setup(self):
        self.client = APIClient

    def test_create_user(self):
        """Test creating a user is successful."""
        result = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=PAYLOAD["email"])
        self.assertTrue(user.check_password(PAYLOAD["password"]))
        self.assertNotIn("password", result.data)

    def test_user_with_email_exist_error(self):
        """Test error returned if user with email exist."""
        create_user(**PAYLOAD)
        result = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error(self):
        """Test error returned if password less than 6 characters."""
        PAYLOAD["password"] = "123"
        result = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=PAYLOAD["email"]).exists()
        self.assertFalse(user_exists)
