from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password


class UserModelBackend(ModelBackend):
    def authenticate(self, username="", password="", **kwargs):
        try:
            user = get_user_model().objects.get(username__iexact=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None
