from django.urls import path
from users.api.views import RequestUserAPIView, UserProfileAPIView

urlpatterns = [
    path("user/", RequestUserAPIView.as_view(), name='user-info'),
    path("profile/<slug:slug>/", UserProfileAPIView.as_view(), name='user-profile')
]
