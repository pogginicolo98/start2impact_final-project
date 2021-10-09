from auctions.models import Auction, AuctionReport
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

    def validate_initial_price(self, value):
        if value == 0:
            return None
        return value


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
    All bids are recorded on Redis, so serializer does not use a Model class.

    * format: JSON.
    """

    price = serializers.DecimalField(max_digits=11, decimal_places=2)

    def validate(self, data):
        request_user = self.context.get('request').user
        auction = self.context.get('auction')
        latest_bid = auction.get_latest_bid()
        if latest_bid is not None:
            is_last_user = bool(request_user.username == latest_bid['user'])
            last_price = latest_bid['price']
        else:
            is_last_user = False
            last_price = auction.initial_price
        if is_last_user:
            raise serializers.ValidationError('Your previous bid is still active.')
        if data['price'] <= last_price:
            raise serializers.ValidationError('Amount must be greater than the current price.')
        return data

class AuctionInfoSerializer(serializers.Serializer):
    """
    Auction serializer for AuctionInfoRetrieveAPIView.

    :fields
    - is_last_user: Is the current user the last one that placed a bid?
    - last_price: price of the last bid placed.

    * format: JSON.
    """

    is_last_user = serializers.SerializerMethodField(read_only=True)
    last_price = serializers.SerializerMethodField(read_only=True)
    remaining_time = serializers.SerializerMethodField(read_only=True)

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

    def get_remaining_time(self, instance):
        auction = self.context.get('auction')
        return auction.get_auction_remaining_time()


class AuctionReportSerializer(serializers.ModelSerializer):
    """
    AuctionReport serializer for AuctionReportRetrieveAPIView.

    :fields
    - json_file

    * format: DATA.
    """

    class Meta:
        model = AuctionReport
        fields = ['json_file']
