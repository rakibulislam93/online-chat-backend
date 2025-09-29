import jwt
from django.conf import settings
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    JWT token এর মাধ্যমে WebSocket authentication
    """

    async def __call__(self, scope, receive, send):
        # Query params থেকে token নেয়া
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token")
        user = None

        if token:
            try:
                payload = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user = await database_sync_to_async(User.objects.get)(id=payload["user_id"])
            except Exception as e:
                print("JWT Auth error:", e)
                user = None

        scope["user"] = user
        return await super().__call__(scope, receive, send)
