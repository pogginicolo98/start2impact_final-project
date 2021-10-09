from auctions.api.views import (AuctionBidAPIView,
                                AuctionClosedListRetrieveAPIView,
                                AuctionImageUpdateAPIView,
                                AuctionInfoRetrieveAPIView,
                                AuctionListRetrieveAPIView,
                                AuctionReportRetrieveAPIView,
                                AuctionScheduleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'schedule-auctions', AuctionScheduleViewSet, basename='schedule-auctions')
router.register(r'auctions', AuctionListRetrieveAPIView, basename='auctions')
router.register(r'closed-auctions', AuctionClosedListRetrieveAPIView, basename='closed-auctions')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule-auctions/<int:pk>/upload-image/', AuctionImageUpdateAPIView.as_view(), name='upload-image'),
    path('auctions/<int:pk>/bid/', AuctionBidAPIView.as_view(), name='auction-bid'),
    path('auctions/<int:pk>/info/', AuctionInfoRetrieveAPIView.as_view(), name='auction-info'),
    path('auctions/closed/<int:pk>/download-report/', AuctionReportRetrieveAPIView.as_view(), name='download-report'),
]
