import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser


class AccountsTestCase(TestCase):
    """
    Accounts urls test case.

    :tests
    - test_login_url_by_name(): Session log in.
    - test_registration_url_by_name(): Session registration.
    """

    homepage_url = reverse('entry-point')
    login_url = reverse('login')
    registration_url = reverse('django_registration_register')

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testcase1', password='Change_me_123!')

    def test_login_url_by_name(self):
        credentials = {
            'username': 'testcase1',
            'password': 'Change_me_123!',
        }
        response = self.client.post(self.login_url, data=credentials, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=self.homepage_url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_registration_url_by_name(self):
        user_count = CustomUser.objects.count()
        credentials = {
            'username': 'testcase2',
            'email': 'testcase2@mail.com',
            'password1': 'Change_me_123!',
            'password2': 'Change_me_123!'
        }
        response = self.client.post(self.registration_url, data=credentials, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=self.homepage_url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )
        self.assertEqual(CustomUser.objects.count(), user_count + 1)


class RESTAuthTestCase(APITestCase):
    """
    Django REST Auth configuration test case.

    :tests
    - test_authentication(): Log in with a user via Django REST Auth APIs.
    - test_registration(): Register a new user via Django REST Auth APIs.
    """

    homepage_url = reverse('entry-point')

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testcase1', password='Change_me_123!')

    def test_authentication(self):
        credentials = {
            'username': 'testcase1',
            'password': 'Change_me_123!'
        }
        response = self.client.post('http://127.0.0.1:8000/api/rest-auth/login/', data=credentials)
        json_response = json.loads(response.content)
        token = f"Token {json_response['key']}"
        headers = {'Authorization': token}
        response = self.client.get(self.homepage_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration(self):
        credentials = {
            'username': 'testcase2',
            'email': 'testcase2@mail.com',
            'password1': 'Change_me_123!',
            'password2': 'Change_me_123!',
        }
        response = self.client.post('/api/rest-auth/registration/', data=credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
