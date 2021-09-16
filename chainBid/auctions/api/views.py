from auctions.api.serializers import AuctionScheduleSerializer
from auctions.models import Auction
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AuctionScheduleViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet:
    - Create a new auction instance.
    - Retrieve a list of all auction instances or a specific one that are not in progress or ended.
    - Update a specific auction instance that is not in progress or ended.
    - Delete a specific auction instance that is not in progress or ended.

    * Only staff users can access to this endpoint.
    """

    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        now = timezone.now()
        queryset = Auction.objects.exclude(enabled=True, opening_date__lte=now, closing_date__gte=now).filter(won_by=None, closing_price=None)
        return queryset
