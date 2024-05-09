import jwt
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_token(request):
    if request.method == 'POST':
        # Extract user ID from request body
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')

        if user_id:
            token = _generate_token(user_id)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def decode_token(request):
    if request.method == 'POST':

        # When decoding the token, 
        # expecting the token to be provided in the request body 
        # (data = request.body.decode('utf-8')).
        # in typical usage, the token is usually sent in the request headers 
        # as an Authorization token. So, you should decode the token 
        # from the request headers instead of the request body

        # Extract token from request headers
        token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None

        if token:
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
                return JsonResponse({'decoded_token': decoded_token})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)
        else:
            return JsonResponse({'error': 'Token not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def _generate_token(user_id):
    # Generate JWT token
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token.decode('utf-8')  # Convert bytes to string for JSON serialization
