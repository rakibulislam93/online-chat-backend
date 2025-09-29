from django.urls import re_path

from . import consumers
websocket_urlspatterns = [
    re_path('ws/chat/(?P<receiver_id>\d+)/$',consumers.ChatConsumer.as_asgi()),
]