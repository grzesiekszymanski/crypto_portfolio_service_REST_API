from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    """This class include tests related with user model."""

    def test_create_user(self):
        """Test user was created successful."""
        email = "testemail@example.com"
        username = "testusername"
        password = "testpassword"

        user = get_user_model().objects.create_user(
            email=email, username=username, password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
