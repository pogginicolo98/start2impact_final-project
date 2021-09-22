import json

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from redis import Redis
from utils.randomics import random_date
from utils.redis_config import IP_ADDRESS, PORT

UserModel = get_user_model()


class Auction(models.Model):
    """
    Auction model.
    Bids are stored and managed on Redis.

    :fields
    - final_price: This filed will be populated only at the end of the auction.
    - status: False=non active, True=active.
    - won_by: This filed will be populated only at the end of the auction.
    """

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    initial_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    opening_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    won_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='auctions', blank=True, null=True)
    final_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'
        ordering = ['-opening_date', 'title']

    def __str__(self):
        return self.title

    def open_auction(self):
        """
        Enable the auction and calculate the maximum closing date.

        :return
        - max_closing_date: Random DateTime between 20 to 24 hours after the opening
        """

        self.status = not self.status
        self.save()
        min_duration = self.opening_date + timezone.timedelta(hours=20)
        max_duration = self.opening_date + timezone.timedelta(hours=24)
        max_closing_date = random_date(start=min_duration, end=max_duration)
        return max_closing_date

    def close_auction(self):
        """
        ???
        """

        self.status = not self.status
        self.closed_at = timezone.now()
        latest_bid = self.get_latest_bid()
        if latest_bid:
            self.won_by = get_object_or_404(UserModel, username=latest_bid['user'])
            self.final_price = latest_bid['price']
        self.save()

    def get_latest_bid(self):
        """
        Get the latest bid placed.

        :return
        - None: If no bid is found.
        - {'user', 'admin', 'price': 9.99}: Sample bid.
        """

        redis_client = Redis(IP_ADDRESS, port=PORT)
        key = f'Auction n.{self.pk} - bids'
        try:
            latest_bid_json = redis_client.lrange(key, 0, 0)[0]
        except IndexError:
            return None
        latest_bid = json.loads(latest_bid_json)
        return latest_bid

    def push_new_bid(self, user, price):
        """
        Record a new bid.
        """

        redis_client = Redis(IP_ADDRESS, port=PORT)
        key = f'Auction n.{self.pk} - bids'
        bid = {
            'user': user,
            'price': price
        }
        value = json.dumps(bid)
        redis_client.lpush(key, value)

    def push_task_id(self, task_id):
        """
        Record the id of the last celery task that is handling the closing of the auction.
        """

        redis_client = Redis(IP_ADDRESS, port=PORT)
        key = f'Auction n.{self.pk} - remaining time'
        value = json.dumps(task_id)
        redis_client.lpush(key, value)

    def pop_task_id(self):
        """
        Get the id of the last celery task that is handling the closing of the auction.
        """

        redis_client = Redis(IP_ADDRESS, port=PORT)
        key = f'Auction n.{self.pk} - remaining time'
        value = json.loads(redis_client.lpop(key))
        return value
