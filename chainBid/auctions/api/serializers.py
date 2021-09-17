from auctions.models import Auction
from redis import Redis
from rest_framework import serializers


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
    - initial_price
    - last_price ???
    - opening_date
    - remaining_time ???

    * format: JSON.
    """

    last_price = serializers.SerializerMethodField(read_only=True)
    remaining_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'opening_date', 'last_price', 'remaining_time']

    def get_last_price(self, instance):
        return '???'

    def get_remaining_time(self, instance):
        return '???'


class AuctionBidSerializer(serializers.Serializer):
    """
    ???
    """

    price = serializers.DecimalField(max_digits=11, decimal_places=2)
    is_last_user = serializers.SerializerMethodField(read_only=True)

    def get_is_last_user(self, instance):
        request_user = self.context.get('request').user
        last_user_bid = self.context.get('redisdb ???')
        return True

    def create(self, validated_data):
        redis_client = Redis('localhost', port=6379)
        key = datetime.now().strftime('%d/%m/%Y')
        value = f"{datetime.now().strftime('%H:%M:%S')} - {request.user} has retrieved a posts list"
        redis_client.lpush(key, value)
