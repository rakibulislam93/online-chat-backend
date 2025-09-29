"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import chat.routing
from chat.middleware import JWTAuthMiddleware
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter(chat.routing.websocket_urlspatterns)
    )
})

