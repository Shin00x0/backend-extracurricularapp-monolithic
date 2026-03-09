from typing import Optional
from django.contrib.auth.hashers import check_password
from users.models import BaseUser


class LocalAuthBackend:
    """Authenticate against local password stored on BaseUser for admin users."""

    def authenticate(self, request, email: Optional[str] = None, password: Optional[str] = None, **kwargs):
        if not email or not password:
            return None

        try:
            user = BaseUser.objects.get(email=email)
        except BaseUser.DoesNotExist:
            return None

        # Only allow local auth for users who are configured for local auth or for staff accounts
        if user.auth_provider != 'local' and not user.is_staff and not user.is_superuser:
            return None

        if not user.password:
            return None

        if check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return BaseUser.objects.get(pk=user_id)
        except BaseUser.DoesNotExist:
            return None
