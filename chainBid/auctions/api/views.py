from auctions.api.serializers import (# AuctionBidSerializer,
                                      AuctionClosedSerializer,
                                      AuctionImageSerializer,
                                      # AuctionInfoSerializer,
                                      AuctionScheduleSerializer,
                                      AuctionSerializer)
from auctions.models import Auction
from auctions.tasks import update_close_auction
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from utils.auction_redis import record_object_on_redis


class AuctionScheduleViewSet(ModelViewSet):
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

    queryset = Auction.objects.filter(closed_at=None).exclude(status=True)
    serializer_class = AuctionScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuctionImageUpdateAPIView(UpdateAPIView):
    """
    Auction image UpdateAPIView.

    :actions
    - update

    * Only staff users can access to this endpoint.
    """

    queryset = Auction.objects.filter(closed_at=None).exclude(status=True)
    serializer_class = AuctionImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuctionListRetrieveAPIView(ListModelMixin,
                                 RetrieveModelMixin,
                                 GenericViewSet):
    """
    Auction ViewSet.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    queryset = Auction.objects.filter(status=True)
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]


# class AuctionBidAPIView(APIView):
#     """
#     Auction's bid APIView.
#
#     :actions
#     - create
#
#     * Only authenticated users can access to this endpoint.
#     """
#
#     serializer_class = AuctionBidSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, pk):
#         serializer_context = {
#             'user': request.user.username,
#             'auction': pk
#         }
#         serializer = self.serializer_class(data=request.data, context=serializer_context)
#         if serializer.is_valid():
#             record_object_on_redis(
#                 auction=pk,
#                 bid_user=request.user.username,
#                 bid_price=float(serializer.data['price'])
#             )
#             update_bid_closing_time(pk=pk)
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class AuctionInfoRetrieveAPIView(RetrieveAPIView):
#     """
#     Auction info RetrieveAPIView.
#
#     :actions
#     - retrieve
#
#     * Only authenticated users can access to this endpoint.
#     """
#
#     queryset = Auction.objects.filter(status=True)
#     serializer_class = AuctionInfoSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['user'] = self.request.user.username
#         context['auction'] = self.get_object().pk
#         return context


class AuctionClosedListRetrieveAPIView(ListModelMixin,
                                       RetrieveModelMixin,
                                       GenericViewSet):
    """
    Auction ViewSet.

    :actions
    - list
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    queryset = Auction.objects.filter(status=False).exclude(closed_at=None)
    serializer_class = AuctionClosedSerializer
    permission_classes = [IsAuthenticated]
