import re
from urllib.parse import urlparse

from django.test import TestCase, override_settings
from django.core import mail
from rest_framework.test import APIClient


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AuthorAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123',
        }

    def test_registration_activation_login_refresh_logout_jwt(self):
        response = self.client.post('/account/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        match = re.search(r'(http://[^\s]+/account/active/[^\s]+/[^\s]+)', body)
        self.assertIsNotNone(match, msg='Activation link not found in email body')
        activation_url = match.group(1)
        if not activation_url.endswith('/'):
            activation_url += '/'

        response = self.client.get(activation_url)
        self.assertIn(response.status_code, (301, 302))
        self.assertEqual(response['Location'], '/account/login/')

        login_response = self.client.post(
            '/account/login/',
            {'username': 'testuser', 'password': 'TestPass123'},
            format='json',
        )
        self.assertEqual(login_response.status_code, 200)
        login_data = login_response.json()
        self.assertIn('access', login_data)
        self.assertIn('refresh', login_data)

        access_token = login_data['access']
        refresh_token = login_data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        create_response = self.client.post('/account/account/', {}, format='json')
        self.assertEqual(create_response.status_code, 201)

        refresh_response = self.client.post(
            '/account/token/refresh/',
            {'refresh': refresh_token},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, 200)
        refresh_data = refresh_response.json()
        self.assertIn('access', refresh_data)
        new_refresh_token = refresh_data.get('refresh', refresh_token)

        logout_response = self.client.post(
            '/account/logout/',
            {'refresh': new_refresh_token},
            format='json',
        )
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json().get('detail'), 'Logout successful.')

        refresh_again_response = self.client.post(
            '/account/token/refresh/',
            {'refresh': new_refresh_token},
            format='json',
        )
        self.assertNotEqual(refresh_again_response.status_code, 200)
