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
