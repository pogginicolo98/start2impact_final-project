from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

UserModel = get_user_model()


class IndexTemplateViewTestCase(TestCase):
    """
    IndexTemplateView test case.

    :tests
    - test_entry_point_url_by_name_not_authenticated(): Access to the homepage by unauthenticated user.
    - test_entry_point_url_by_name_authenticated(): Access to the homepage by authenticated user.
    """

    homepage_url = reverse('entry-point')

    def setUp(self):
        self.user = UserModel.objects.create_user(username='testcase', password='Change_me_123!')

    def test_entry_point_url_by_name_not_authenticated(self):
        expected_url = reverse('login') + "?next=" + self.homepage_url
        response = self.client.get(self.homepage_url)  # Ex. URL: http://127.0.0.1/
        self.assertRedirects(
            response=response,
            expected_url=expected_url,  # Ex. URL: http://127.0.0.1/accounts/login/?next=/
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_entry_point_url_by_name_authenticated(self):
        self.client.login(username='testcase', password='Change_me_123!')
        response = self.client.get(self.homepage_url)  # Ex. URL: http://127.0.0.1/
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if settings.DEBUG:
            self.assertTemplateUsed(response, 'index-dev.html')
        else:
            self.assertTemplateUsed(response, 'index.html')
