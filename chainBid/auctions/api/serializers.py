from auctions.models import Auction
from rest_framework import serializers


class AuctionScheduleSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionScheduleViewSet.

    :fields
    - title
    - description
    - initial_price
    - opening_date
    """

    class Meta:
        model = Auction
        fields = ['title', 'description', 'initial_price', 'opening_date']


class AuctionSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionViewSet.

    :fields
    - title
    - description
    - image
    - opening_price
    - current_price
    - opening_date
    - duration
    """

    pass
