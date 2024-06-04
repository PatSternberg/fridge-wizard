# file: backend/middleware/auth_middleware.py
from django.http import JsonResponse
from .auth import decode_token
from .user_manager import get_user_by_id

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token_string = request.headers.get('Authorization', '')[7:]

        try:
            decoded_token = decode_token(token_string)
            user_id = decoded_token.get('user_id')
            user = get_user_by_id(user_id)

            if user:
                request.user_id = user_id
                return self.get_response(request)
            else:
                return JsonResponse({'message': 'Invalid user'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'Authentication error'}, status=401)