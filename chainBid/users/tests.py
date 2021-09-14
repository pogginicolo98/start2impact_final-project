from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser


class AccountsTestCase(TestCase):
    """
    Accounts test case.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testcase1', password='Change_me_123!')
        self.homepage_url = reverse('entry-point')
        self.login_url = reverse('login')
        self.registration_url = reverse('django_registration_register')

    def test_login_url_by_name(self):
        data = {
            'username': 'testcase1',
            'password': 'Change_me_123!',
        }
        response = self.client.post(self.login_url, data=data, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=self.homepage_url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_registration_url_by_name(self):
        user_count = CustomUser.objects.count()
        data = {
            'username': 'testcase2',
            'email': 'testcase2@mail.com',
            'password1': 'Change_me_123!',
            'password2': 'Change_me_123!'
        }
        response = self.client.post(self.registration_url, data=data, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=self.homepage_url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )
        self.assertEqual(CustomUser.objects.count(), user_count + 1)
