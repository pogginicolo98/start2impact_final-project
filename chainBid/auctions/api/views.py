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

    * Only authenticated users can retrieve a list of all 'ProfileStatus' instances or a specific one.
    * Users can update only their own 'ProfileStatus' instances.
    * Authentication via token by REST Auth.
    """

    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Override 'get_queryset()' method of GenericAPIView class.
        Retrieve 2 lists of 'ProfileStatus' instances.
        - Retrieve a list with all 'ProfileStatus' instances if request has no parameters.
        - Retrieve a list with all 'ProfileStatus' instances that correspond to the user passed as parameter in the request.
        """

        now = timezone.now()
        queryset = Auction.objects.exclude(enabled=True, opening_date__lte=now, closing_date__gte=now).filter(won_by=None, closing_price=None)
        return queryset
