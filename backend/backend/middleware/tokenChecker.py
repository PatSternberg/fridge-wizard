
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..lib.token import decode_token


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract token from Authorization header
        token_string = request.headers.get('Authorization', '')[7:]

        # Decode and validate token
        try:
            decoded_token = decode_token(token_string)
            user_id = decoded_token.get('userID')

            # Check if user exists
            user = user.objects.get(id=user_id)

            # Store user ID in request for later use
            request.user_id = user_id

            # Continue with request processing
            return self.get_response(request)
        except Exception as e:
            # Handle authentication errors
            return JsonResponse({'message': 'Authentication error'}, status=401)
