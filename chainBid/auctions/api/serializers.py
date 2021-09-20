from auctions.models import Auction
from rest_framework import serializers
from utils.bids import get_latest_bid


class AuctionScheduleSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionScheduleViewSet.

    :fields
    - title
    - description
    - image
    - initial_price
    - opening_date

    * format: JSON.
    """

    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'opening_date']


class AuctionImageSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionImageUpdateAPIView.

    :fields
    - image

    * format: DATA.
    """

    class Meta:
        model = Auction
        fields = ['image']


class AuctionSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionViewSet.

    :fields
    - title
    - description
    - image
    - last_price ???
    - opening_date
    - remaining_time ???

    * format: JSON.
    """

    last_price = serializers.SerializerMethodField(read_only=True)
    remaining_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        exclude = ['initial_price', 'final_price', 'closing_date', 'status', 'won_by', 'created_at', 'updated_at']

    def get_last_price(self, instance):
        try:
            latest_bid = get_latest_bid(auction=instance)
        except IndexError:
            return instance.initial_price
        return latest_bid.get('price')

    def get_remaining_time(self, instance):
        return '???'


class AuctionBidSerializer(serializers.Serializer):
    """
    Bid serializer for AuctionBidAPIView.
    All bids are recorded on Redis, so Serializer does not use a Model class.

    :fields
    - price: New price.
    - is_last_user: Is the current user the last one that placed a bid?
    - last_price: price of the last bid placed.

    * format: JSON.
    """

    price = serializers.DecimalField(max_digits=11, decimal_places=2)
    is_last_user = serializers.SerializerMethodField(read_only=True)
    last_price = serializers.SerializerMethodField(read_only=True)

    def get_is_last_user(self, instance):
        request_user = self.context.get('request').user
        auction = self.context.get('auction')
        try:
            latest_bid = get_latest_bid(auction=auction)
        except IndexError:
            return False
        return bool(request_user.username == latest_bid.get('user'))

    def get_last_price(self, instance):
        # If no offers have been placed yet, then return the initial_price
        auction = self.context.get('auction')
        try:
            latest_bid = get_latest_bid(auction=auction)
        except IndexError:
            return auction.initial_price
        return latest_bid.get('price')
