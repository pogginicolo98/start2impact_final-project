import json

from auctions.api.serializers import AuctionScheduleSerializer, AuctionSerializer
from auctions.models import Auction
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

UserModel = get_user_model()


class OrderViewSetTestCase(APITestCase):
    """
    AuctionScheduleViewSet test case.

    :actions
    - list
    - create
    - retrieve
    - update
    - delete

    * Only staff users can access to this endpoint.
    """

    def setUp(self):
        """
        Create new users, get an authentication token and authenticate the staff user.
        Create an auction for tests and setup urls.
        """
        self.staff_user = UserModel.objects.create_user(username='testcase1', password='Change_me_123!', is_staff=True)
        self.common_user = UserModel.objects.create_user(username='testcase2', password='Change_me_123!')
        self.auction = Auction.objects.create(
            title='Test auction 1',
            description='some text...',
            initial_price=10.99,
            opening_date=timezone.now(),
        )
        self.list_url = reverse('schedule-auctions-list')
        self.detail_url = reverse('schedule-auctions-detail', kwargs={'pk': self.auction.pk})
        self.token = Token.objects.create(user=self.staff_user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_auctions_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_auctions_non_staff(self):
        self.client.force_authenticate(user=self.common_user)
        response = self.client.get(self.list_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_auctions_authenticated(self):
        response = self.client.get(self.list_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_auction_not_authenticated(self):
        data = {'title': 'Test auction 2'}
        self.client.force_authenticate(user=None)
        response = self.client.post(self.list_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_auction_non_staff(self):
        data = {'title': 'Test auction 2'}
        self.client.force_authenticate(user=self.common_user)
        response = self.client.post(self.list_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_auction_authenticated(self):
        opening_date = timezone.now()
        data = {
            'title': 'Test auction 2',
            'description': 'some text...',
            'initial_price': 20.99,
            'opening_date': opening_date
        }
        response = self.client.post(self.list_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['title'], 'Test auction 2')  # Checking the fully rendered response
        self.assertEqual(json_response['description'], 'some text...')  # Checking the fully rendered response
        self.assertEqual(json_response['initial_price'], '20.99')  # Checking the fully rendered response

    def test_retrieve_auction_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auction/1/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_auction_non_staff(self):
        self.client.force_authenticate(user=self.common_user)
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auction/1/
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_auction_authenticated(self):
        serializer_data = AuctionScheduleSerializer(instance=self.auction).data
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auction/1/
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, serializer_data)  # Checking the fully rendered response

    def test_update_auction_not_authenticated(self):
        data = {'title': 'Test auction updated'}
        self.client.force_authenticate(user=None)
        response = self.client.put(self.detail_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_auction_non_staff(self):
        data = {'title': 'Test auction updated'}
        self.client.force_authenticate(user=self.common_user)
        response = self.client.put(self.detail_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_auction_authenticated(self):
        data = {'title': 'Test auction updated'}
        response = self.client.put(self.detail_url, data=data)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['title'], 'Test auction updated')  # Checking the fully rendered response
        self.assertEqual(json_response['initial_price'], '10.99')  # Checking the fully rendered response

    def test_delete_auction_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_auction_non_staff(self):
        self.client.force_authenticate(user=self.common_user)
        response = self.client.delete(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_auction_authenticated(self):
        response = self.client.delete(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/schedule-auctions/1/
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuctionListRetrieveAPIViewTestCase(APITestCase):
    """
    AuctionListRetrieveAPIView test case.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    def setUp(self):
        """
        Create new user, get an authentication token and authenticate with it.
        Create an auction for tests and setup urls.
        """
        self.user = UserModel.objects.create_user(username='testcase', password='Change_me_123!')
        self.auction1 = Auction.objects.create(
            title='Test auction 1',
            description='some text...',
            initial_price=10.99,
            opening_date=timezone.now(),
            status=True
        )
        self.auction2 = Auction.objects.create(
            title='Test auction 2',
            description='some text...',
            initial_price=10.99,
            opening_date=timezone.now()
        )
        self.list_url = reverse('auctions-list')
        self.detail_url = reverse('auctions-detail', kwargs={'pk': self.auction1.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_auctions_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)  # Ex. URL: http://127.0.0.1/api/auctions/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_auctions_authenticated(self):
        serializer_data = AuctionSerializer(instance=self.auction1).data
        response = self.client.get(self.list_url)  # Ex. URL: http://127.0.0.1/api/auctions/
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['count'], 1)  # Checking the fully rendered response
        self.assertEqual(json_response['results'][0], serializer_data)  # Checking the fully rendered response

    def test_retrieve_auction_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/auction/1/
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_auction_authenticated(self):
        serializer_data = AuctionSerializer(instance=self.auction1).data
        response = self.client.get(self.detail_url)  # Ex. URL: http://127.0.0.1/api/auction/1/
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, serializer_data)  # Checking the fully rendered response
