from auctions.models import Auction, AuctionReport
from django.utils import timezone
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
        fields = ['id', 'title', 'description', 'image', 'opened_at', 'initial_price', 'last_price', 'remaining_time']

    def get_last_price(self, instance):
        bid = instance.get_latest_object_on_redis(type_obj='bids')
        if bid is not None:
            return bid['price']
        return instance.initial_price

    def get_remaining_time(self, instance):
        task = instance.get_latest_object_on_redis(type_obj='close')
        if task is not None:
            if task['eta'] is not None:
                delta = task['eta'] - timezone.now()
                return delta.seconds
        return None

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
        bid = auction.get_latest_object_on_redis(type_obj='bids')
        if bid is not None:
            is_last_user = bool(request_user.username == bid['user'])
            last_price = bid['price']
        else:
            is_last_user = False
            last_price = auction.initial_price
        if is_last_user:
            raise serializers.ValidationError('Your previous bid is still active.')
        if data['price'] <= last_price:
            raise serializers.ValidationError('Price must be higher than the current price.')
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
        bid = auction.get_latest_object_on_redis(type_obj='bids')
        if bid is not None:
            return bool(request_user.username == bid['user'])
        return False

    def get_last_price(self, instance):
        # If no offers have been placed yet, then return the initial_price
        auction = self.context.get('auction')
        bid = auction.get_latest_object_on_redis(type_obj='bids')
        if bid is not None:
            return bid['price']
        return auction.initial_price

    def get_remaining_time(self, instance):
        auction = self.context.get('auction')
        task = auction.get_latest_object_on_redis(type_obj='close')
        if task is not None:
            if task['eta'] is not None:
                delta = task['eta'] - timezone.now()
                return delta.seconds
        return None


# class AuctionReportSerializer(serializers.ModelSerializer):
#     """
#     AuctionReport serializer for AuctionReportRetrieveAPIView.
#
#     :fields
#     - json_file
#
#     * format: DATA.
#     """
#
#     class Meta:
#         model = AuctionReport
#         fields = ['json_file']


class AuctionClosedSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionClosedListRetrieveAPIView.

    :fields
    - title
    - description
    - image
    - initial_price
    - final_price
    - winner
    - opened_at
    - closed_at
    - json_file

    * format: JSON.
    """

    winner = serializers.SerializerMethodField(read_only=True)
    json_file = serializers.SerializerMethodField(read_only=True)
    hash = serializers.SerializerMethodField(read_only=True)
    tx_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        exclude = ['status']

    def get_winner(self, instance):
        return str(instance.winner)

    def get_json_file(self, instance):
        request = self.context.get("request")
        if instance.report.json_file:
            return request.build_absolute_uri(instance.report.json_file.url)
        return None

    def get_hash(self, instance):
        if instance.report.hash:
            return instance.report.hash
        return None

    def get_tx_id(self, instance):
        if instance.report.tx_id:
            return instance.report.tx_id
        return None
