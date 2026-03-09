import pytest
from django.test import RequestFactory
from django.urls import reverse
from unittest.mock import patch

from core.middleware.firebase_middleware import FirebaseAuthMiddleware
from users.models import BaseUser


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.django_db
def test_middleware_attaches_user_on_valid_token(rf):
    request = rf.get(reverse('users:user-profile'))
    request.META['HTTP_AUTHORIZATION'] = 'Bearer validtoken'

    # Mock firebase service verify_token to return a decoded payload
    fake_decoded = {'uid': 'uid-123', 'email': 'fuser@example.com', 'name': 'Fake User'}

    with patch('core.middleware.firebase_middleware.get_firebase_service') as get_svc:
        get_svc.return_value.verify_token.return_value = fake_decoded

        # Create and run middleware
        mw = FirebaseAuthMiddleware(lambda req: (req, True))
        new_request, _ = mw(request)

        # After middleware, request.user should be created/attached
        assert hasattr(new_request, 'user')
        assert isinstance(new_request.user, BaseUser)
        assert new_request.user.firebase_uid == 'uid-123'
        assert new_request.user.email == 'fuser@example.com'
        assert getattr(new_request, 'firebase_user') == fake_decoded


@pytest.mark.django_db
def test_middleware_ignores_when_no_auth_header(rf):
    request = rf.get(reverse('users:user-profile'))

    mw = FirebaseAuthMiddleware(lambda req: (req, True))
    new_request, _ = mw(request)

    # No auth header -> user should remain absent or AnonymousUser
    assert not hasattr(new_request, 'firebase_user')
