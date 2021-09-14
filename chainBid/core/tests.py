from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser


class IndexTemplateViewTestCase(TestCase):
    """
    IndexTemplateView test case.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testcase', password='Change_me_123!')
        self.url = reverse('entry-point')

    def test_entry_point_url_by_name_by_not_authenticated_user(self):
        expected_url = reverse('login') + "?next=" + self.url
        response = self.client.get(self.url)
        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_entry_point_url_by_name_by_authenticated_user(self):
        self.client.login(username='testcase', password='Change_me_123!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if settings.DEBUG:
            self.assertTemplateUsed(response, 'index-dev.html')
        else:
            self.assertTemplateUsed(response, 'index.html')
