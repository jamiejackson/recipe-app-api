"""
Tests for modles.
"""

from django.test import TestCase
# provided by Django to access default user model
#  best to use this because if the user model is changed in the future,
#  this will still work
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        # check_password is a method provided by Django's User model to verify
        #  the password, since passwords are hashed
        self.assertTrue(user.check_password(password))
