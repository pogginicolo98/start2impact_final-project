from auctions.models import Auction
from django.utils import timezone
from rest_framework import serializers
from utils.auction_redis import auction_started, BIDS_KEY, get_latest_object_on_redis


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
        latest_bid = get_latest_object_on_redis(auction=instance.pk, type_obj=BIDS_KEY)
        if latest_bid is not None:
            return latest_bid['price']
        return instance.initial_price

    def get_remaining_time(self, instance):
        latest_bid = get_latest_object_on_redis(auction=instance.pk, type_obj=BIDS_KEY)
        if latest_bid is not None:
            if latest_bid.get('eta', None) is not None:
                delta = latest_bid['eta'] - timezone.now()
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
        user = self.context.get('user')
        auction_pk = self.context.get('auction')
        if auction_started(auction=auction_pk):
            latest_bid = get_latest_object_on_redis(auction=auction_pk, type_obj=BIDS_KEY)
            if user == latest_bid['user']:
                raise serializers.ValidationError('Your previous bid is still active.')
            if data['price'] <= latest_bid['price'] or data['price'] <= 0:
                raise serializers.ValidationError('Price must be higher than the current price.')
        else:
            raise serializers.ValidationError('Auction not available.')
        return data


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
