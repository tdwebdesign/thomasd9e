from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value for the token.
        Include the user's primary key, last login, and timestamp.
        """
        return str(user.pk) + str(timestamp) + str(user.date_joined)


account_activation_token = AccountActivationTokenGenerator()
