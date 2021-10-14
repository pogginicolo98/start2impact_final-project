import hashlib
import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from redis import Redis
from utils.decoders import DateTimeDecoder
from utils.encoders import AuctionEncoder
from utils.randomics import random_date
from utils.transactions import write_message_on_chain

UserModel = get_user_model()


class Auction(models.Model):
    """
    Auction model.
    Bids are stored and managed on Redis.

    :fields
    - final_price: This filed will be populated only at the end of the auction.
    - status: False=non active, True=active.
    - winner: This filed will be populated only at the end of the auction.
    """

    # Generic config
    REDIS_HOST = settings.REDIS_HOST
    REDIS_PORT = settings.REDIS_PORT
    IMAGES_DIR = 'auction images'

    # Fields
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=240, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=IMAGES_DIR, default=os.path.join(IMAGES_DIR, 'image_empty.png'))
    initial_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    final_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='auctions', blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'
        ordering = ['-opened_at', 'title']

    def __str__(self):
        return self.title

    def open_auction(self):
        """
        Perform the following actions:
        1) Enable the auction.
        2) Set the close_auction() task to run on a random date between 20 to 24 hours after the opening.
        """

        min_duration = self.opened_at + timezone.timedelta(hours=20)
        max_duration = self.opened_at + timezone.timedelta(hours=24)
        max_closing_date = random_date(start=min_duration, end=max_duration)
        self.status = True
        self.save()
        return max_closing_date

    def close_auction(self):
        """
        Perform the following actions:
        1) Disable the auction.
        2) Store the winning bid's data.
        3) Remove bids data from Redis.
        """

        self.status = False
        self.closed_at = timezone.now()
        latest_bid = self.get_latest_bid()
        if latest_bid is not None:
            self.winner = get_object_or_404(UserModel, username=latest_bid['user'])
            self.final_price = latest_bid['price']
        self.save()
        self.clean_db()

    def add_bid(self, user, price):
        """
        Record a new bid.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - bids'
        bid = {
            'user': user,
            'price': price
        }
        value = json.dumps(bid)
        redis_client.lpush(key, value)

    def get_latest_bid(self):
        """
        Get the latest bid placed.

        :return
        - None: If no bid is found.
        - Bid: {'user', user.username, 'price': Float object}.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - bids'
        value = redis_client.lrange(key, 0, 0)
        if value is not None and len(value) > 0:
            return json.loads(value[0])
        return None

    def add_close_auction_task(self, task_id, eta=None):
        """
        Record the id and eta of the last celery task that is handling the closing of the auction.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - remaining time'
        task = {
            'task_id': task_id,
            'eta': eta
        }
        value = json.dumps(task, cls=AuctionEncoder)
        redis_client.lpush(key, value)

    def get_latest_close_auction_task(self):
        """
        Get the id and eta of the last celery task that is handling the closing of the auction.

        :return
        - None: If no task is found.
        - Task: {'task_id': celery task id, 'eta': DateTime object}.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - remaining time'
        value = redis_client.lrange(key, 0, 0)
        if value is not None and len(value) > 0:
            return json.loads(value[0], cls=DateTimeDecoder)
        return None

    def add_schedule_task(self, task_id):
        """
        Record the id of the celery task that is handling the opening of the auction.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - schedule'
        task = {'task_id': task_id}
        value = json.dumps(task)
        redis_client.lpush(key, value)

    def get_latest_schedule_task(self):
        """
        Get the id of the celery task that is handling the opening of the auction.

        :return
        - None: If no task is found.
        - task_id
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key = f'Auction n.{self.pk} - schedule'
        value = redis_client.lrange(key, 0, 0)
        if value is not None and len(value) > 0:
            return json.loads(value[0])
        return None

    def clean_db(self):
        """
        Delete bids and related data from Redis db.
        """

        redis_client = Redis(self.REDIS_HOST, port=self.REDIS_PORT)
        key1 = f'Auction n.{self.pk} - bids'
        key2 = f'Auction n.{self.pk} - remaining time'
        key3 = f'Auction n.{self.pk} - schedule'
        redis_client.delete(key1, key2, key3)


class AuctionReport(models.Model):
    """
    Auction report model.
    """

    # Generic config
    MEDIA_DIR = settings.MEDIA_ROOT

    # Fields
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE, related_name='report')
    json_file = models.FileField(blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True, null=True)
    tx_id = models.CharField(max_length=66, blank=True, null=True)

    def make_report(self):
        """
        Make a json report and write it on the Ethereum blockchain.

        Json file: 'auction x.json'.
        Network: Ropsten.
        """

        report = {
            'title': self.auction.title,
            'description': self.auction.description,
            'initial price': self.auction.initial_price,
            'final price': self.auction.final_price,
            'winner': str(self.auction.winner),
            'opened at': self.auction.opened_at,
            'closed at': self.auction.closed_at
        }
        file_name = f'auction {self.auction.pk}.json'
        destination_dir = os.path.join(self.MEDIA_DIR, 'reports')
        path = os.path.join(destination_dir, file_name)
        try:
            os.mkdir(destination_dir)
        except OSError:
            pass  # Already exists
        with open(path, 'w') as f:
            json.dump(report, f, cls=AuctionEncoder)
        self.json_file = os.path.join('reports', file_name)
        self.hash = hashlib.sha256(json.dumps(report, cls=AuctionEncoder).encode('utf-8')).hexdigest()
        self.tx_id = write_message_on_chain(self.hash)
        self.save()
