from auctions.models import Auction
from django.utils import timezone
from rest_framework import serializers


class AuctionScheduleSerializer(serializers.ModelSerializer):
    """
    Auction serializer for AuctionScheduleViewSet.

    :fields
    - title
    - description
    - opening_price
    - opening_date
    - closing_date
    - enabled
    """

    class Meta:
        model = Auction
        exclude = ['image', 'closing_price', 'won_by', 'created_at', 'updated_at']

    def validate(self, data):
        now = timezone.now()

        if data['opening_date'] and data['closing_date']:
            if data['opening_date'] > data['closing_date']:
                raise serializers.ValidationError('The opening date must come before the closing date')

        if data['enabled']:
            if not data['opening_date'] or not data['closing_date']:
                raise serializers.ValidationError('In order to enable the auction, both the opening date and the closing date must be set')
            elif data['opening_date'] <= now:
                raise serializers.ValidationError('You cannot enable an auction that should have already started')
        return data
