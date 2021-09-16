from auctions.api.views import AuctionImageUpdateAPIView, AuctionListRetrieveAPIView, AuctionScheduleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'schedule-auctions', AuctionScheduleViewSet, basename='schedule-auctions')
router.register(r'auctions', AuctionListRetrieveAPIView, basename='auctions')

urlpatterns = [
    path('', include(router.urls)),
    path('schedule-auctions/<int:pk>/upload-image/', AuctionImageUpdateAPIView.as_view(), name='upload-image'),
]
