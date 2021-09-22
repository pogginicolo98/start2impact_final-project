from auctions.api.serializers import (AuctionBidSerializer,
                                      AuctionImageSerializer,
                                      AuctionScheduleSerializer,
                                      AuctionSerializer)
from auctions.models import Auction
from auctions.signals import auction_bid_apiview_called
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
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

    serializer_class = AuctionImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        kwarg_pk = self.kwargs.get('pk')
        auction_object = get_object_or_404(Auction, pk=kwarg_pk)
        return auction_object


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


class AuctionBidAPIView(APIView):
    """
    Auction's bid APIView.

    :actions
    - create
    - retrieve

    * Only authenticated users can access to this endpoint.
    """

    serializer_class = AuctionBidSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        if auction.status:
            latest_bid = auction.get_latest_bid()
            if latest_bid:
                is_last_user = bool(request.user.username == latest_bid.get('user'))
                last_price = latest_bid.get('price')
            else:
                is_last_user = False
                last_price = auction.initial_price
            response_data = {
                'is_last_user': is_last_user,
                'last_price': last_price,
                'remaining_time': '???'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        error = {'detail': 'Auction not available'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        if auction.status:
            serializer_context = {
                'request': request,
                'auction': auction
            }
            serializer = self.serializer_class(data=request.data, context=serializer_context)
            if serializer.is_valid():
                auction.push_new_bid(
                    user=request.user.username,
                    price=float(serializer.data.get('price'))
                )
                # Send signal in order to update the auction's remaining time
                auction_bid_apiview_called.send(sender='auction-bid-api-view', instance=auction)
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error = {'detail': 'Auction not available'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
