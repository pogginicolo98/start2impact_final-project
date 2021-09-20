import json

from auctions.api.serializers import (AuctionBidSerializer,
                                      AuctionImageSerializer,
                                      AuctionScheduleSerializer,
                                      AuctionSerializer)
from auctions.models import Auction
from django.shortcuts import get_object_or_404
from redis import Redis
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

    queryset = Auction.objects.filter(closing_date=None).exclude(status=True)
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

    * Only authenticated users can access to this endpoint.
    """

    serializer_class = AuctionBidSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pass

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        if auction.status:
            serializer_context = {
                'request': request,
                'auction': auction
            }
            serializer = self.serializer_class(data=request.data, context=serializer_context)
            if serializer.is_valid():
                redis_client = Redis('localhost', port=6379)
                key = f'Auction n.{auction.pk}'
                bid = {
                    'user': request.user.username,
                    'price': float(serializer.data.get('price'))
                }
                value = json.dumps(bid)
                redis_client.lpush(key, value)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error = {'detail': 'Auction not available'}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
