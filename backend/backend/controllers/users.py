import json
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from utility.db_handler import DBHandler
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from bson.errors import InvalidId
from backend.middleware.validator import Validator
from auth.auth import generate_token
from pymongo import MongoClient

@csrf_exempt # Disables CSRF protection for this view
def signup(request):
    if request.method == 'POST':
        print("Received signup request:", request.body)
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Initialize validator
        validator = Validator()

        try:
            # Validate password
            validator.validate_password(password)
            print("Password validated successfully")
            # Validate email
            validator.validate_email(email)
            print("Email validated successfully")

            # # Get the database handle
            # db, client = DBHandler.get_db_handle(db_name=settings.DB_NAME,
            #                                      host=settings.HOST,
            #                                      port=settings.MONGODB_PORT,
            #                                      username='',
            #                                      password='')

            # users_collection = db['users']

                        # Get the URI from settings.py
            uri = settings.MONGODB_URI
            # Create a MongoClient instance with the provided URI
            client = MongoClient(uri)
            print(client)
            # Get the database from the client
            db = client[settings.DB_NAME]
            print(db)
            
            users_collection = db['users']

            # if the email already exists
            if users_collection.find_one({'email': email}):
                return JsonResponse({'error': 'Email already in use.'}, status=400)

            # Insert the new user
            user_id = users_collection.insert_one({
                'username': username,
                'email': email,
                'password': password
            }).inserted_id

            # Clean up: close the MongoDB client
            client.close()

            return JsonResponse({'message': 'User created successfully', 'user_id': str(user_id)}, status=201)
        except ValidationError as e:
            # Validation failed
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Get the database handle
        db, client = DBHandler.get_db_handle(db_name=settings.DB_NAME,
                                                host=settings.HOST,
                                                port=settings.MONGODB_PORT,
                                                username='',
                                                password='')

        users_collection = db['users']

        try:
            # Retrieve the user from the database
            user = users_collection.find_one({'email': email})
            if not user:
                # User not found
                return JsonResponse({'error': 'User not found'}, status=404)
            
            # Check if the password matches
            if password != user['password']:
                # Password incorrect
                return JsonResponse({'error': 'Password incorrect'}, status=401)
            
            # Generate token for the authenticated user
            token = generate_token(user['_id'])

            # Clean up: close the MongoDB client
            client.close()

            # Return token along with user_id
            return JsonResponse({'message': 'Login successful', 'user_id': str(user['_id']), 'token': token}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_user(request):
    # Check if GET method in request
    if request.method == 'GET':
        # Get the user id supplied as a parameter with the GET request
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'user_id parameter is missing'}, status=400)
        
        # Get the database handle
        db, client = DBHandler.get_db_handle(db_name=settings.DB_NAME,
                                                host=settings.HOST,
                                                port=settings.MONGODB_PORT,
                                                username='',
                                                password='')

        users_collection = db['users']
        
        try:
            # Access the users collection
            users_collection = db['users']

            # Find the user by _id
            user_data = users_collection.find_one({'_id': ObjectId(user_id)})

            client.close()

            # Check if the user data exists
            if user_data:
                # Convert ObjectId to string before serializing to JSON
                user_data['_id'] = str(user_data['_id'])
                return JsonResponse({'user_data': user_data}, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except InvalidId:
            return JsonResponse({'error': 'Invalid user ID'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
