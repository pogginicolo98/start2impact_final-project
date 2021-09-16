from auctions.api.views import AuctionScheduleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'schedule', AuctionScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]
