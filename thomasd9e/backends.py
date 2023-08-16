from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class CaseInsensitiveEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # If multiple entries have the same email address, take the first one.
            user = (
                UserModel.objects.filter(email__iexact=username).order_by("id").first()
            )

        if user.check_password(password):
            return user
        return None
