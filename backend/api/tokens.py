"""Utils for creating a token."""
from api.models import Administrator

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import six


class TokenGenerator(PasswordResetTokenGenerator):
    """Token generator for user registration."""

    def _make_hash_value(self, user: Administrator, timestamp: int) -> str:
        """Hashes user information.

        Args:
            user: user to hash
            timestamp: current moment of time, is set automatically

        Returns:
            str: hashed information of the user
        """
        return (
            six.text_type(user.id) + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
