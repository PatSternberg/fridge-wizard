from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from pymongo import MongoClient
from .users import PasswordValidator, EmailValidator
import json
from django.conf import settings

def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(host=host, port=int(port), username=username, password=password)
    db_handle = client[db_name]
    return db_handle, client


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        if not user_id:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

        # Get the database handle
        db, client = get_db_handle(db_name='fridge_hero',
                                    host='localhost',
                                    port=27017,
                                    username='',
                                    password='')

        # Replace the above lines with the following to use MongoDB Atlas
        # Get the URI from settings.py
        uri = settings.MONGODB_URI
        # Create a MongoClient instance with the provided URI
        client = MongoClient(uri)
        # Get the database from the client
        db = client[settings.DB_NAME]

        users_collection = db['users']

        try:
            # Retrieve the user from the database
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            if not user:
                # User not found
                return JsonResponse({'error': 'User not found'}, status=404)

            messages = []

            if email and user.get('email') != email:
                #Validate email
                email_validator = EmailValidator()
                email_validator.validate(email)
                
                # Update email
                user['email'] = email
                messages.append('Email updated successfully')

            if password and user.get('password') != password:
                # Validate password
                password_validator = PasswordValidator()
                password_validator.validate(password)

                # Update password
                user['password'] = password
                messages.append('Password updated successfully')

            if username and user.get('username') != username:
                # Update username
                user['username'] = username
                messages.append('Username updated successfully')

            # Save the updated user data back to the database
            users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': user})

            # Clean up: close the MongoDB client
            client.close()

            return JsonResponse({'message': ', '.join(messages)})
        except ValidationError as e:
            # Validation failed
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
