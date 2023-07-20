"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


TOKEN_URL = reverse("user:token")
CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:me")
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
        self.client = APIClient()

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
        tmp_payload = {
            "email": "test_email@example.com",
            "username": "test_username",
            "password": "123",
        }
        result = self.client.post(CREATE_USER_URL, tmp_payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=tmp_payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        create_user(**PAYLOAD)
        result = self.client.post(TOKEN_URL, PAYLOAD)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIn("token", result.data)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        tmp_payload = {
            "email": "test_email@example.com",
            "username": "test_username",
            "password": "incorrect_password",
        }
        create_user(**PAYLOAD)
        result = self.client.post(TOKEN_URL, tmp_payload)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        tmp_payload = {
            "email": "test_email@example.com",
            "username": "test_username",
            "password": "",
        }
        result = self.client.post(TOKEN_URL, tmp_payload)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that requires authentication."""

    def setUp(self):
        self.user = create_user(
            email="test_email@example.com",
            username="test_username",
            password="test_password",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        result = self.client.get(ME_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result.data, {"email": self.user.email, "username": self.user.username}
        )

    def test_post_me_not_allowed(self):
        """The POST is not allowed for the 'me' endpoint."""
        result = self.client.post(ME_URL, {})

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile fpr the authenticated user."""
        payload = {
            "username": "new_username",
            "email": "new_email@example.com",
            "password": "new_password",
        }
        result = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.username, payload["username"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)
