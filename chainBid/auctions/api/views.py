from auctions.api.serializers import (AuctionBidSerializer,
                                      AuctionClosedSerializer,
                                      AuctionImageSerializer,
                                      AuctionInfoSerializer,
                                      AuctionScheduleSerializer,
                                      AuctionSerializer)
from auctions.models import Auction
from auctions.signals import auction_bid_apiview_called
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet


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


class AuctionBidAPIView(APIView):
    """
    Auction's bid APIView.

    :actions
    - create

    * Only authenticated users can access to this endpoint.
    """

    serializer_class = AuctionBidSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        if auction.status:
            serializer_context = {
                'request': request,
                'auction': auction
            }
            serializer = self.serializer_class(data=request.data, context=serializer_context)
            if serializer.is_valid():
                auction.record_object_on_redis(
                    bid_user=request.user.username,
                    bid_price=float(serializer.data.get('price'))
                )
                # Send signal in order to update the auction's remaining time
                auction_bid_apiview_called.send(sender='auction-bid-api-view', instance=auction)
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error = {'detail': 'Not found.'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class AuctionInfoRetrieveAPIView(RetrieveAPIView):
    """
    Auction info RetrieveAPIView.

    :actions
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    queryset = Auction.objects.filter(status=True)
    serializer_class = AuctionInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['auction'] = self.get_object()
        return context


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
