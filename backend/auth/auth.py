# file: backend/auth/auth.py
import jwt
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .user_manager import get_user_by_credentials

@csrf_exempt
def create_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = get_user_by_credentials(username, password)
        if user:
            token = generate_token(str(user['_id']))
            return JsonResponse({'token': token, 'user_id': str(user['_id'])}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def decode_token(request):
    if request.method == 'POST':
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

def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token