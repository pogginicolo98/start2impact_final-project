from auctions.api.serializers import AuctionImageSerializer, AuctionScheduleSerializer, AuctionSerializer
from auctions.models import Auction
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AuctionScheduleViewSet(viewsets.ModelViewSet):
    """
    Auction schedule CRUD ViewSet.

    :actions
    - list
    - create
    - retrieve
    - update
    - delete

    * Only staff users can access to this endpoint.
    """

    queryset = Auction.objects.filter(closing_date=None).exclude(status=True)
    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuctionImageUpdateAPIView(generics.UpdateAPIView):
    """
    Auction image UpdateAPIView.

    :actions
    - update

    * Only staff users can access to this endpoint.
    """

    serializer_class = AuctionImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        kwarg_pk = self.kwargs.get('pk')
        auction_object = get_object_or_404(Auction, pk=kwarg_pk)
        return auction_object


class AuctionListRetrieveAPIView(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """
    Auction ViewSet.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Two types of queryset:
        - List with all auction instances.
        - Specific auction instance.
        """

        queryset = Auction.objects.filter(status=True)
        kwarg_pk = self.kwargs.get('pk', None)
        if kwarg_pk is not None:
            queryset = queryset.filter(pk=kwarg_pk)
        return queryset
