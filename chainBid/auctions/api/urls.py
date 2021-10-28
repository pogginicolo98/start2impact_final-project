from auctions.api.views import (AuctionClosedListRetrieveAPIView,
                                AuctionImageUpdateAPIView,
                                AuctionListRetrieveAPIView,
                                AuctionScheduleViewSet,
                                UserAuctionClosedListAPIView)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'schedule-auctions', AuctionScheduleViewSet, basename='schedule-auctions')
router.register(r'auctions', AuctionListRetrieveAPIView, basename='auctions')
router.register(r'closed-auctions', AuctionClosedListRetrieveAPIView, basename='closed-auctions')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule-auctions/<int:pk>/upload-image/', AuctionImageUpdateAPIView.as_view(), name='upload-image'),
    path('user-closed-auctions/', UserAuctionClosedListAPIView.as_view(), name='user-closed-auctions'),
]
