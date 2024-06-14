# file: fridge-wizard/backend/tests/users_test.py
import unittest
import os
import django
import json
from pymongo import MongoClient
from django.test import RequestFactory
from backend.controllers.users import signup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Comments below outline all intended tests, not necessarily completed
# Test Signup Function:
class UserSignupTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.users_collection = self.db['users']
        self.users_collection.delete_many({})  # Ensure collection is empty

    def tearDown(self):
        # Drop the test database
        self.client.drop_database(os.getenv('TEST_DB_NAME'))
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
        
        # Cleanup: Remove the user manually from the collection
        self.users_collection.delete_one({'email': 'testUserValid@example.com'})

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
        print(f"{response_data['message']}")

        # Cleanup: Remove the user manually from the collection
        self.users_collection.delete_one({'email': 'testUserExisting@example.com'})

# Test case for attempting to sign up with an invalid email format
# Test case for attempting to sign up with an invalid password (e.g., too short, no special characters, etc.)
# Test case for handling unexpected exceptions during signup

# Test Login Function:

# Test case for successful user login with valid credentials
# Test case for attempting to log in with an email that doesn't exist
# Test case for attempting to log in with an incorrect password
# Test case for handling unexpected exceptions during login

# Test Get User Function:

# Test case for retrieving user data with a valid user ID
# Test case for attempting to retrieve user data with an invalid user ID
# Test case for handling the case when no user_id parameter is provided
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