# Backup of original users/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from users.models import BaseUser


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:user-profile')

    def test_profile_requires_auth(self):
        resp = self.client.get(self.url)
        # Depending on authentication classes (SessionAuth + CSRF) this
        # endpoint may return 401 (Unauthorized) or 403 (Forbidden). Accept both.
        self.assertIn(resp.status_code, (401, 403))

    def test_profile_returns_user_data_when_authenticated(self):
        user = BaseUser.objects.create(email='test@example.com', name='Test User')
        self.client.force_authenticate(user=user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        data = resp.data.get('data')
        self.assertIsNotNone(data)
        self.assertEqual(data.get('email'), 'test@example.com')
        self.assertEqual(data.get('id'), str(user.id))