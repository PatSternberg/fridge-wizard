# file: fridge-wizard/backend/tests/users_test.py
import unittest
import os
import django
import json
from pymongo import MongoClient
from django.test import RequestFactory
from backend.controllers.users import signup, login, get_user

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Comments below outline all intended tests, not necessarily completed
# Test Signup Function:
class UserSignupTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        try:
            # establish connection to MongoDB
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('TEST_DB_NAME')]
            self.users_collection = self.db['users']
            # Clean up any existing test users
            self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
        except Exception as e:
            print(f"Database connection error: {e}")
            self.fail("Failed to connect to the database")

    def tearDown(self):

        # Cleanup: Remove any user manually from the collection
        self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
        # close connection to MongoDB
        self.client.close()
        
    # Test case for successful user signup with valid input data
    def test_valid_user_signup(self):
        # User data
        valid_user_data = {
            'username': 'testUserValid',
            'email': 'testUserValid@example.com',
            'password': 'testPasswordValid!'
        }

        # Create POST request
        request_body = json.dumps(valid_user_data)
        request = self.factory.post('/signup', request_body, content_type='application/json')

        # Call signup function
        response = signup(request)

        # Assert response
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
        self.assertIn('user_id', response_data)
        self.assertEqual(response_data['message'], 'User created successfully')
        print(f"{response_data['message']}")

    # Test case for attempting to sign up with an email that already exists
    def test_duplicate_email_signup(self):
        # User data
        existing_user_data = {
            'username': 'testUserExisting',
            'email': 'testUserExisting@example.com',
            'password': 'testPasswordExisting!'
        }

        # Create initial POST request to simulate existing user
        request_body = json.dumps(existing_user_data)
        request = self.factory.post('/signup', request_body, content_type='application/json')

        # Call signup function for existing user
        response = signup(request)

        # Assert response for existing user
        self.assertEqual(response.status_code, 201)
        
        # Call signup function again to test duplicate email handling
        response = signup(request)
        
        # Assert response for duplicate email
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Email already in use.')
        print(f"{response_data['error']}")

    # Test case for attempting to sign up with an invalid email format
    def test_invalid_email_signup(self):
        # User data
        existing_user_data = {
            'username': 'testUserValid',
            'email': 'testUserInvalidEmail',
            'password': 'testValidPassword!'
        }

        # Create initial POST request to simulate existing user
        request_body = json.dumps(existing_user_data)
        request = self.factory.post('/signup', request_body, content_type='application/json')

        # Call signup function for existing user
        response = signup(request)
        
        # Assert response for duplicate email
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "['Invalid email format.']")
        print(f"{response_data['error']}")

    # Test case for attempting to sign up with an invalid password (e.g. no special characters)
    def test_invalid_password_signup_no_special_character(self):
        # User data
        existing_user_data = {
            'username': 'testUserValid',
            'email': 'testUserValid@example.com',
            'password': 'testInvalidPassword'
        }

        # Create initial POST request to simulate existing user
        request_body = json.dumps(existing_user_data)
        request = self.factory.post('/signup', request_body, content_type='application/json')

        # Call signup function for existing user
        response = signup(request)
        
        # Assert response for duplicate email
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "['This password must contain at least one special character.']")
        print(f"{response_data['error']}")

    # Test case for attempting to sign up with an invalid password (e.g. too short)
    def test_invalid_password_signup_too_short(self):
        # User data
        existing_user_data = {
            'username': 'testUserValid',
            'email': 'testUserValid@example.com',
            'password': 'Invalid'
        }

        # Create initial POST request to simulate existing user
        request_body = json.dumps(existing_user_data)
        request = self.factory.post('/signup', request_body, content_type='application/json')

        # Call signup function for existing user
        response = signup(request)
        
        # Assert response for duplicate email
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "['This password must contain at least 8 characters.']")
        print(f"{response_data['error']}")

# Test Login Function:
class UserLoginTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        try:
            # establish connection to MongoDB
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('TEST_DB_NAME')]
            self.users_collection = self.db['users']
            # Clean up any existing test users
            self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
            # Add a test user to the database
            self.test_user = {
                'username': 'testUser',
                'email': 'testUserValid@example.com',
                'password': 'testPassword123!'
            }
            self.users_collection.insert_one(self.test_user)

        except Exception as e:
            print(f"Database connection error: {e}")
            self.fail("Failed to connect to the database")

    def tearDown(self):

        # Cleanup: Remove any user manually from the collection
        self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
        # close connection to MongoDB
        self.client.close()

    # Test case for successful user login with valid credentials
    def test_valid_user_login(self):
        # User data
        valid_user_data = {
            'email': 'testUserValid@example.com',
            'password': 'testPassword123!'
        }

        # Create POST request
        request_body = json.dumps(valid_user_data)
        request = self.factory.post('/login', request_body, content_type='application/json')

        # Call login function
        response = login(request)

        # Assert response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
        self.assertIn('user_id', response_data)
        self.assertIn('token', response_data)
        self.assertEqual(response_data['message'], 'Login successful')
        print(f"{response_data['message']}")

    # Test case for attempting to log in with an email that doesn't exist
    def test_valid_user_login_invalid_email(self):
        # User data
        valid_user_data = {
            'email': 'invalidTestUser@example.com',
            'password': 'testPassword123!'
        }

        # Create POST request
        request_body = json.dumps(valid_user_data)
        request = self.factory.post('/login', request_body, content_type='application/json')

        # Call login function
        response = login(request)

        # Assert response
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertNotIn('token', response_data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'User not found')
        print(f"{response_data['error']}")

    # Test case for attempting to log in with an incorrect password
    def test_valid_user_login_invalid_password(self):
        # User data
        valid_user_data = {
            'email': 'testUserValid@example.com',
            'password': 'testInvalidPassword123!'
        }

        # Create POST request
        request_body = json.dumps(valid_user_data)
        request = self.factory.post('/login', request_body, content_type='application/json')

        # Call login function
        response = login(request)

        # Assert response
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content)
        self.assertNotIn('token', response_data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Password incorrect')
        print(f"{response_data['error']}")

# Test Get User Function:
# Test case for retrieving user data with a valid user ID
class GetUserTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        try:
            # establish connection to MongoDB
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('TEST_DB_NAME')]
            self.users_collection = self.db['users']
            # Clean up any existing test users
            self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
            # Add a test user to the database
            self.test_user = {
                'username': 'testUser',
                'email': 'testUserValid@example.com',
                'password': 'testPassword123!'
            }
            self.users_collection.insert_one(self.test_user)
            
        except Exception as e:
            print(f"Database connection error: {e}")
            self.fail("Failed to connect to the database")

    def tearDown(self):

        # Cleanup: Remove any user manually from the collection
        self.users_collection.delete_many({'email': {'$regex': '^testUser'}})
        # close connection to MongoDB
        self.client.close()

    # Test case for successful user login with valid credentials
    def test_get_valid_user(self):
        # Get the test user ID
        test_user_id = str(self.users_collection.find_one({'email': 'testUserValid@example.com'})['_id'])

        # Create GET request with user_id as query parameter
        request = self.factory.get('/get-user', {'user_id': test_user_id})

        # Call get_user function
        response = get_user(request)

        # Assert response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('user_data', response_data)
        print(f"{response_data['user_data']}")

    # Test case for attempting to retrieve user data with an invalid user ID
    def test_get_invalid_user(self):
        # Get the test user ID
        test_user_id = str(self.users_collection.find_one({'email': 'testUserValid@example.com'})['_id'])

        # Create GET request with user_id as query parameter
        request = self.factory.get('/get-user', {'user_id': f'{test_user_id}Invalid'})

        # Call get_user function
        response = get_user(request)

        # Assert response
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        print(f"{response_data['error']}")

    # Test case for handling the case when no user_id parameter is provided
    def test_get_no_user_id(self):
        # Get the test user ID
        test_user_id = ''

        # Create GET request with user_id as query parameter
        request = self.factory.get('/get-user', {'user_id': test_user_id})

        # Call get_user function
        response = get_user(request)

        # Assert response
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        print(f"{response_data['error']}")

# Test case for handling unexpected exceptions during user data retrieval

# Test Validator:

# Test case for validating a valid email
# Test case for validating an invalid email
# Test case for validating a valid password
# Test case for validating an invalid password

# Test DBHandler:

# Test case for successfully establishing a connection to the MongoDB database
# Test case for handling the case when the MongoDB connection fails

# Test Token Generation:

# Test case for generating a valid token for a given user ID
# Test case for handling unexpected exceptions during token generation

# Test Error Handling:

# Test cases for verifying that appropriate error responses are returned with the correct status codes for different error scenarios (e.g., method not allowed, missing parameters, etc.)


# Test CSRF Protection:

# Test case for verifying that the CSRF protection is disabled for the signup and login views


# Test Data Sanitization:

# Test case for ensuring that user input data is properly sanitized and validated before being processed


# Test Database Cleanup:

# Test case for verifying that the MongoDB client is properly closed after each operation

if __name__ == '__main__':
    unittest.main()