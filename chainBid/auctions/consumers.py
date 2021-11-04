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
    Bid consumer WebsocketConsumer.
    Receive new bids and record them on Redis than
    echo new bids to all users connected to the same auction.

    :events
    - echo_bid_info: Send the new bid's info to users who monitor the same auction.
    - auction_closed: Notify the end of the auction.

    :Channel groups
    - Auction slug: Channel for each available auction.

    * Only authenticated users can send (receive action for consumer) new bids.
    * Every user can receive (send action for consumer) bid's updates.
    """

    user = None
    auction = None
    channel_group = None

    def connect(self):
        """
        Reject connections that refers to auctions that are no longer available.
        When a user connects, he immediately receives information about the latest bid.
        """

        self.user = async_to_sync(get_user)(self.scope)
        self.auction = self.scope['url_route']['kwargs']['slug']
        self.channel_group = self.auction
        latest_bid = self.get_latest_bid(auction=self.auction)
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
        """
        Accept, validate and execute new bids if the user is authenticated.
        """

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
                bid = self.get_latest_bid(auction=self.auction)
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
        """
        Echo bid info event.
        When a new bid is placed automatically echo the information about it to the users connected.
        """

        self.send(text_data=json.dumps({
            'is_last_user': bool(self.user.username == event.get('user', None)),
            'last_price': event['price'],
            'remaining_time': event.get('remaining_time', None)
        }))

    def auction_closed(self, event):
        """
        Auction closed event.
        Notify users who are following an auction when it closes.
        """

        self.send(text_data=json.dumps({
            'closed': True,
            'is_winner': bool(self.user.username == event.get('winner', None))
        }))

    def accept_new_bid(self, auction, user, price):
        """
        Validate and execute a new bid.
        """

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
            update_close_auction(slug=auction, eta=eta)
            return None
        else:
            return serializer.errors

    def get_latest_bid(self, auction):
        """
        Get latest bid.
        """

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
