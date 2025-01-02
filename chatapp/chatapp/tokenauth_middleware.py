


# from channels.middleware import BaseMiddleware
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser

# @database_sync_to_async
# def get_user_from_token(token_key):
#     # Import Token model here to avoid loading it prematurely
#     from rest_framework.authtoken.models import Token

#     try:
#         token = Token.objects.get(key=token_key)
#         return token.user
#     except Token.DoesNotExist:
#         return AnonymousUser()

# class TokenAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         scope['user'] = AnonymousUser()

#         headers = dict(scope['headers'])
#         if b'authorization' in headers:
#             try:
#                 token_name, token_key = headers[b'authorization'].decode().split()
#                 if token_name == 'Token':
#                     scope['user'] = await get_user_from_token(token_key)
#             except ValueError:
#                 pass  # Malformed token, default to AnonymousUser

#         # Print user info
#         print(f'User Info on middleware: {vars(scope["user"])}')

#         return await super().__call__(scope, receive, send)

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs

@database_sync_to_async
def get_user_from_token(token_key):
    from rest_framework.authtoken.models import Token
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = AnonymousUser()

        # Check for token in headers
        headers = dict(scope['headers'])
        token_key = None
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name != 'Token':
                    token_key = None
            except ValueError:
                pass  # Malformed header

        # Check for token in query string if not in headers
        if not token_key:
            query_params = parse_qs(scope.get("query_string", b"").decode())
            token_key = query_params.get("token", [None])[0]

        # Authenticate the user
        if token_key:
            scope['user'] = await get_user_from_token(token_key)

        # Print user info for debugging
        print(f'User Info on middleware: {vars(scope["user"])}')

        return await super().__call__(scope, receive, send)
