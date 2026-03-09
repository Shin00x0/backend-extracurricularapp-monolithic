import pytest
from django.urls import reverse
from unittest.mock import patch
from users.models import BaseUser


@pytest.mark.django_db
def test_profile_endpoint_with_firebase_token(client):
    url = reverse('users:user-profile')

    fake_decoded = {'uid': 'uid-999', 'email': 'intuser@example.com', 'name': 'Integration User'}

    # Patch both the middleware's and the DRF auth class's firebase service
    with patch('core.middleware.firebase_middleware.get_firebase_service') as get_svc_mw, \
         patch('core.utils.firebase.get_firebase_service') as get_svc_utils:
        get_svc_mw.return_value.verify_token.return_value = fake_decoded
        get_svc_utils.return_value.verify_token.return_value = fake_decoded

        resp = client.get(url, HTTP_AUTHORIZATION='Bearer valid-token')

        assert resp.status_code == 200
        assert resp.json().get('success') is True
        data = resp.json().get('data')
        assert data['email'] == 'intuser@example.com'

        # Ensure user was created in DB and linked
        user = BaseUser.objects.get(firebase_uid='uid-999')
        assert user.email == 'intuser@example.com'
