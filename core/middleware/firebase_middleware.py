"""Middleware to authenticate requests using Firebase ID tokens in Authorization header."""
from typing import Optional
import logging

from django.contrib.auth.models import AnonymousUser

from core.utils.firebase import get_firebase_service
from users.models import BaseUser

logger = logging.getLogger(__name__)


class FirebaseAuthMiddleware:
    """Middleware that verifies Firebase ID tokens and attaches a BaseUser.

    Behavior:
    - If `request.user` is already authenticated (session-based), middleware does nothing.
    - If an Authorization: Bearer <token> header is present and token verifies,
      it will attach or create a `BaseUser` and set `request.user` to that user.
    - It also sets `request.firebase_user` (decoded token dict) and `request.firebase_token`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
                return self.get_response(request)

            auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()

            if auth_header and len(auth_header) == 2 and auth_header[0] == 'Bearer':
                token = auth_header[1]
                firebase_service = get_firebase_service()
                decoded = firebase_service.verify_token(token)

                if decoded:
                    uid = decoded.get('uid')
                    email = decoded.get('email') or ''

                    try:
                        user = BaseUser.objects.get(firebase_uid=uid)
                    except BaseUser.DoesNotExist:
                        user = BaseUser.objects.create(
                            firebase_uid=uid,
                            email=email or f"{uid}@firebase.local",
                            name=decoded.get('name', ''),
                        )

                    request.user = user
                    request.firebase_user = decoded
                    request.firebase_token = token
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("FirebaseAuthMiddleware error: %s", exc)

        return self.get_response(request)
