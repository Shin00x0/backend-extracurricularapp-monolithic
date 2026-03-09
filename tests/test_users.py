import pytest
from django.urls import reverse
from users.models import BaseUser


@pytest.mark.django_db
def test_profile_requires_auth(api_client):
    url = reverse('users:user-profile')
    resp = api_client.get(url)
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_profile_returns_user_data_when_authenticated(api_client):
    url = reverse('users:user-profile')
    user = BaseUser.objects.create(email='test@example.com', name='Test User')
    api_client.force_authenticate(user=user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data.get('success')
    data = resp.data.get('data')
    assert data is not None
    assert data.get('email') == 'test@example.com'
    assert data.get('id') == str(user.id)
