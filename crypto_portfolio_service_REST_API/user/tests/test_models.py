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

    def test_email_normalized(self):
        """Verify whether email normalization works as expected."""
        emails_to_test = [
            ["tEsT_eMaIl@example.Com", "user1"],
            ["TEST_EMAIL@EXAMPLE.com", "user2"],
            ["test_email@example.COM", "user3"],
        ]

        normalized_email_fragment = "@example.com"

        for test_email, username in emails_to_test:
            user = get_user_model().objects.create_user(
                test_email, username, "test_password"
            )
            expected_email = test_email[0:10] + normalized_email_fragment
            self.assertEqual(user.email, expected_email)