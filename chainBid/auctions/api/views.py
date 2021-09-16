from auctions.api.serializers import AuctionScheduleSerializer
from auctions.models import Auction
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

    queryset = Auction.objects.filter(closing_date=None).exclude(status=True)
    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
