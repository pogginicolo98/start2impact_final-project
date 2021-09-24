from auctions.models import Auction
from rest_framework import serializers


class AuctionScheduleSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionScheduleViewSet.

    :fields
    - title
    - description
    - image
    - initial_price
    - opened_at

    * format: JSON.
    """

    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'opened_at']


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
    - last_price
    - opened_at
    - remaining_time

    * format: JSON.
    """

    last_price = serializers.SerializerMethodField(read_only=True)
    remaining_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'image', 'opened_at', 'last_price', 'remaining_time']

    def get_last_price(self, instance):
        latest_bid = instance.get_latest_bid()
        if latest_bid is not None:
            return latest_bid['price']
        return instance.initial_price

    def get_remaining_time(self, instance):
        return instance.get_auction_remaining_time()


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
        latest_bid = auction.get_latest_bid()
        if latest_bid is not None:
            return bool(request_user.username == latest_bid['user'])
        return False

    def get_last_price(self, instance):
        # If no offers have been placed yet, then return the initial_price
        auction = self.context.get('auction')
        latest_bid = auction.get_latest_bid()
        if latest_bid is not None:
            return latest_bid['price']
        return auction.initial_price

    def validate(self, data):
        is_last_user = self.get_is_last_user(None)
        last_price = self.get_last_price(None)
        if is_last_user:
            raise serializers.ValidationError('You cannot place another bid')
        elif data['price'] <= last_price:
            raise serializers.ValidationError('The price must be larger than the current price')
        return data
