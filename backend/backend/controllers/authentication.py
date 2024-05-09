from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json
from bson.objectid import ObjectId  # Import ObjectId for working with MongoDB ObjectIDs
from ..lib.token import generate_token  


# we dont' have a Django model for user data,
# won't be able to directly access the user data using Django's 
# built-in User model. I add get_db_handle in authentication 


def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(host=host, port=int(port), username=username, password=password)
    db_handle = client[db_name]
    return db_handle, client

@csrf_exempt
def create_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        db, client = get_db_handle(db_name='fridge-hero', host='localhost', port=27017, username='', password='')
        users_collection = db['users']

        # Find the user by username and password
        user = users_collection.find_one({'username': username, 'password': password})

        if user:
            # If user is found, generate token using user's ObjectId
            token = generate_token(str(user['_id']))  # Assuming '_id' is the ObjectId of the user document
            client.close()

        # return the token and user ID in the response.
            return JsonResponse({'token': token, 'user_id': str(user['_id'])}, status=200)
        else:
            client.close()
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
