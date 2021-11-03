from django.urls import re_path
from auctions.consumers import BidConsumer

websocket_urlpatterns = [
    re_path(r'ws/auctions/(?P<slug>[-\w]+)/bid/$', BidConsumer.as_asgi()),
]
