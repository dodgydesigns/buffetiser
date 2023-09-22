"""
Tests for Models.
"""


from unittest import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test core models."""

    def test_create_user_with_email_successful(self):
        """Test successful creation of user."""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

        user.delete()

    def test_new_user_email_normalise(self):
        """Test that all emails (usernames) entered adhere to the rules."""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "example_pass_123")
            self.assertEqual(user.email, expected)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        """Creating a user without a valid email raises an error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")

    def test_create_superuser(self):
        """Test the creation of a superuser."""

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "testpass123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

        user.delete()
