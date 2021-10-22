import hashlib
import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from utils.auction_redis import BIDS_KEY, clean_db, get_latest_object_on_redis, record_object_on_redis, TASKS_KEY
from utils.encoders_decoders import AuctionEncoder
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

    def open(self):
        """
        Perform the following actions:
        1) Initialize redis in order to accept new bids.
        2) Enable the auction.
        3) Set the close_auction() task to run on a random date between 20 to 24 hours after the opening.
        """

        record_object_on_redis(
            auction=self.pk,
            user=None,
            price=float(self.initial_price)
        )
        self.status = True
        self.save()

    def close(self):
        """
        Perform the following actions:
        1) Disable the auction.
        2) Store the winning bid's data.
        3) Remove bids data from Redis.
        """

        self.status = False
        self.closed_at = timezone.now()
        latest_bid = get_latest_object_on_redis(auction=self.pk, type_obj=BIDS_KEY)
        if latest_bid is not None:
            if latest_bid.get('user', None):
                self.winner = get_object_or_404(UserModel, username=latest_bid['user'])
                self.final_price = latest_bid.get('price', None)
        self.save()


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
            'winner': None,
            'opened at': self.auction.opened_at,
            'closed at': self.auction.closed_at
        }
        if self.auction.winner:
            report['winner'] = self.auction.winner.username
        file_name = f'auction {self.auction.pk}.json'
        reports_dir = 'reports'
        destination_dir = os.path.join(self.MEDIA_DIR, reports_dir)
        path = os.path.join(destination_dir, file_name)
        try:
            os.mkdir(destination_dir)
        except OSError:
            pass  # Already exists
        with open(path, 'w') as f:
            json.dump(report, f, cls=AuctionEncoder)
        self.json_file.name = os.path.join(reports_dir, file_name)
        self.hash = hashlib.sha256(json.dumps(report, cls=AuctionEncoder).encode('utf-8')).hexdigest()
        # self.tx_id = write_message_on_chain(self.hash)
        self.save()
