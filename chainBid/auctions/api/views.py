from auctions.api.serializers import (AuctionClosedSerializer,
                                      AuctionImageSerializer,
                                      AuctionScheduleSerializer,
                                      AuctionSerializer,
                                      UserAuctionClosedSerializer)
from auctions.models import Auction
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class AuctionScheduleViewSet(ModelViewSet):
    """
    Auction schedule CRUD ViewSet.
    Manage scheduled auctions.

    :actions
    - list
    - create
    - retrieve
    - update
    - delete

    * Only staff users can access to this endpoint.
    """

    queryset = Auction.objects.filter(closed_at=None).exclude(status=True).order_by('-opened_at', 'title')
    lookup_field = "slug"
    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuctionImageUpdateAPIView(UpdateAPIView):
    """
    Auction image UpdateAPIView.
    Update the image of a specific auction.

    :actions
    - update

    * Only staff users can access to this endpoint.
    """

    queryset = Auction.objects.filter(closed_at=None).exclude(status=True)
    lookup_field = "slug"
    serializer_class = AuctionImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuctionListRetrieveAPIView(ListModelMixin,
                                 RetrieveModelMixin,
                                 GenericViewSet):
    """
    Auction ListRetrieveAPIView.
    Retrieve all live auctions.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    queryset = Auction.objects.filter(status=True).order_by('-opened_at', 'title')
    lookup_field = "slug"
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]


class AuctionClosedListRetrieveAPIView(ListModelMixin,
                                       RetrieveModelMixin,
                                       GenericViewSet):
    """
    Auction ListRetrieveAPIView.
    Retrieve all closed auctions.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    queryset = Auction.objects.filter(status=False).exclude(closed_at=None).order_by('-closed_at', 'title')
    lookup_field = "slug"
    serializer_class = AuctionClosedSerializer
    permission_classes = [IsAuthenticated]


class UserAuctionClosedListAPIView(ListAPIView):
    """
    Auction ListAPIView.
    Retrieve all auctions won by a specific user.

    :actions
    - list

    * Only authenticated users can access to this endpoint.
    """

    serializer_class = UserAuctionClosedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug_user = self.kwargs.get('slug')
        return Auction.objects.filter(status=False, winner__slug=kwarg_slug_user).order_by('-closed_At', 'title')
