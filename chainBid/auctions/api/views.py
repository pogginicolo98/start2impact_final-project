from auctions.api.serializers import AuctionImageSerializer, AuctionScheduleSerializer
from auctions.models import Auction
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
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


class AuctionImageUpdateAPIView(generics.UpdateAPIView):
    """
    An APIView that provides 'update()' action.
    Update 'avatar' field of a 'Profile' instance.
    * Users can only update their own 'avatar' and must be authenticated.
    * Authentication via token by REST Auth.
    """

    serializer_class = AuctionImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        kwarg_pk = self.kwargs.get('pk')
        auction_object = get_object_or_404(Auction, pk=kwarg_pk)
        return auction_object
