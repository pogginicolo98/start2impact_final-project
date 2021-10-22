import json

from asgiref.sync import async_to_sync
from auctions.api.serializers import AuctionBidSerializer
from auctions.tasks import update_close_auction
from channels.auth import get_user
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from utils.auction_redis import BIDS_KEY, get_latest_object_on_redis, record_object_on_redis


class BidConsumer(WebsocketConsumer):
    """
    Bid consumer AsyncWebsocketConsumer.
    Receive new bids and record them on Redis and
    echo new bids to all users connected to the same auction.

    :events
    - echo_bid_info: Send the new bid's info to users who monitor the same auction.
    - auction_closed: Notify the end of the auction.

    * Only authenticated users can send (receive action for consumer) new bids.
    * Every user receive (send action for consumer) bid's updates.
    """

    user = None
    auction = None
    channel_group = None

    def connect(self):
        self.user = async_to_sync(get_user)(self.scope)
        self.auction = self.scope['url_route']['kwargs']['pk']
        self.channel_group = f'auction_{self.auction}'
        latest_bid = self.get_bid(auction=self.auction)
        if latest_bid is not None:
            async_to_sync(self.channel_layer.group_add)(
                self.channel_group,
                self.channel_name
            )
            self.accept()
            self.send(text_data=json.dumps({
                'is_last_user': bool(self.user.username == latest_bid.get('user', None)),
                'last_price': latest_bid['price'],
                'remaining_time': latest_bid.get('remaining_time', None)
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group,
            self.channel_name
        )
        print("disconnected")

    def receive(self, text_data=None, bytes_data=None):
        if self.user.is_authenticated:
            data_json = json.loads(text_data)
            price = data_json['price']
            errors = self.accept_new_bid(
                auction=self.auction,
                user=self.user.username,
                price=price
            )
            if errors:
                self.send(text_data=json.dumps({'errors': errors}))
            else:
                bid = self.get_bid(auction=self.auction)
                if bid is not None:
                    async_to_sync(self.channel_layer.group_send)(
                        self.channel_group,
                        {
                            'type': 'echo_bid_info',
                            'user': bid.get('user', None),
                            'price': bid['price'],
                            'remaining_time': bid.get('remaining_time', None)
                        }
                    )
                else:
                    self.send(text_data=json.dumps({'errors': 'Auction not available.'}))
        else:
            self.send(text_data=json.dumps({'errors': 'User not authenticated.'}))

    def echo_bid_info(self, event):
        self.send(text_data=json.dumps({
            'is_last_user': bool(self.user.username == event.get('user', None)),
            'last_price': event['price'],
            'remaining_time': event.get('remaining_time', None)
        }))

    def auction_closed(self, event):
        self.send(text_data=json.dumps({
            'closed': True,
            'is_winner': bool(self.user.username == event.get('winner', None))
        }))

    def accept_new_bid(self, auction, user, price):
        serializer_context = {
            'user': user,
            'auction': auction
        }
        serializer = AuctionBidSerializer(data={'price': price}, context=serializer_context)
        if serializer.is_valid():
            eta = timezone.now() + timezone.timedelta(seconds=10)
            record_object_on_redis(
                auction=auction,
                user=user,
                price=float(serializer.data['price']),
                eta=eta
            )
            update_close_auction(pk=auction, eta=eta)
            return None
        else:
            return serializer.errors

    def get_bid(self, auction):
        remaining_time = None
        latest_bid = get_latest_object_on_redis(auction=auction, type_obj=BIDS_KEY)
        if latest_bid is not None:
            user = latest_bid.get('user', None)
            if latest_bid.get('eta', None) is not None:
                delta = latest_bid['eta'] - timezone.now()
                remaining_time = delta.seconds
            bid = {
                'user': user,
                'price': latest_bid['price'],
                'remaining_time': remaining_time
            }
            return bid
        return None
