# file: ./tests/db_test.py
import unittest
import os
import django
import jwt
from pymongo import MongoClient
from datetime import datetime, timedelta
from utility.db_handler import DBHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class MongoDBConnectionTest(unittest.TestCase):
    def setUp(self):
        # establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DB_NAME')]

    def tearDown(self):
        # close connection to MongoDB
        self.client.close()

    def test_MongoDB_connection(self):
        try:
            client = MongoClient(os.getenv('MONGODB_URI'))
            db = client[os.getenv('DB_NAME')]

            # execute a ping command to check connection
            db.command('ping')

            client.close()

            # Print test result
            print("Test 'test_MongoDB_connection' passed successfully.")

        except Exception as e:
            print("Error:", e)
            self.fail("Connection to MongoDB failed.")

class MongoTestDBConnectionTest(unittest.TestCase):
    def setUp(self):
        # establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]

    def tearDown(self):
        # close connection to MongoDB
        self.client.close()

    def test_MongoTestDB_connection(self):
        try:
            # replace these values with test MongoDB details
            client = MongoClient(os.getenv('MONGODB_URI'))
            db = client[os.getenv('TEST_DB_NAME')]

            # execute a ping command to check connection
            db.command('ping')

            client.close()

            # Print test result
            print("Test 'test_MongoTestDB_connection' passed successfully.")

        except Exception as e:
            print("Error:", e)
            self.fail("Connection to MongoDB failed.")

class DBHandlerTest(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['users']

    def tearDown(self):
        # Clean up MongoDB
        self.db.drop_collection('users')
        self.client.close()

    def test_get_db_handle(self):
        # Define the test data
        db_data = {
            "db_name": "test_db",
            "host": "localhost",
            "port": 27017,
            "username": "test_user",
            "password": "test_password",
        }

        # Call the `get_db_handle` method
        db_handle, client = DBHandler.get_db_handle(
            db_name=db_data["db_name"],
            host=db_data["host"],
            port=db_data["port"],
            username=db_data["username"],
            password=db_data["password"]
        )

        # Assert that the returned values are not None
        self.assertIsNotNone(db_handle)
        self.assertIsNotNone(client)

        # Assert that the database name is correct
        self.assertEqual(db_handle.name, db_data["db_name"])

        # Close the client connection
        client.close()

        # Print test result
        print("Test 'test_get_db_handle' passed successfully.")

class DBCreateUserTest(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['users']

    def tearDown(self):

        # Cleanup: Remove any user manually from the collection
        self.collection.delete_many({'email': {'$regex': '^testUser'}})
        # close connection to MongoDB
        self.client.close()

    def test_signup_user(self):
        # define the creation of a user
        user_data = {
            "_id": "testId",
            "username": "testUser",
            "password": "testPassword1",
            "email" : "testUserEmail"
        }

        # add the new user document to the DB
        self.collection.insert_one(user_data)

        # retrieve user document from DB
        retrieved_document = self.collection.find_one({"_id": "testId"})

        # Assert that the retrieved document matches the test document
        self.assertEqual(retrieved_document["_id"], user_data["_id"])
        self.assertEqual(retrieved_document["username"], user_data["username"])
        self.assertEqual(retrieved_document["password"], user_data["password"])
        # retrieved_document["email"] = "diffemail@abc.com"
        self.assertEqual(retrieved_document["email"], user_data["email"])

        
        # Print test result
        print("Test 'test_signup_user' passed successfully.")

class DBUserLoginTest(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['users']

    def tearDown(self):
        # Cleanup: Remove any user manually from the collection
        self.collection.delete_many({'email': {'$regex': '^testUser'}})
        # close connection to MongoDB
        self.client.close()

    def simulate_login_request(self, login_data):
        # Simulate the login process
        db = self.db
        users_collection = db['users']
        
        try:
            # Retrieve the user from the database
            user = users_collection.find_one({'email': login_data['email']})
            if not user:
                # User not found
                return {'status': 404, 'data': {'error': 'User not found'}}
            
            # Check if the password matches
            if login_data['password'] != user['password']:
                # Password incorrect
                return {'status': 401, 'data': {'error': 'Password incorrect'}}
            
            # Generate token for the authenticated user
            token = self.generate_token(user['_id'])

            # Return token along with user_id
            return {'status': 200, 'data': {'message': 'Login successful', 'user_id': str(user['_id']), 'token': token}}
        except Exception as e:
            return {'status': 500, 'data': {'error': f'Something went wrong: {str(e)}'}}

    def generate_token(self, user_id):
        payload = {
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

    def test_login_user(self):
        # define the creation of a user
        user_data = {
            "_id": "testId",
            "username": "testUser",
            "password": "testPassword1",
            "email" : "testUserEmail"
        }

        # add the new user document to the DB
        self.collection.insert_one(user_data)

        # retrieve user document from DB
        retrieved_document = self.collection.find_one({"_id": "testId"})

        # Assert that the retrieved document matches the test document
        self.assertEqual(retrieved_document["_id"], user_data["_id"])
        self.assertEqual(retrieved_document["username"], user_data["username"])
        self.assertEqual(retrieved_document["password"], user_data["password"])
        # retrieved_document["email"] = "diffemail@abc.com"
        self.assertEqual(retrieved_document["email"], user_data["email"])

        # Simulate a login request
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        response = self.simulate_login_request(login_data)

        # Assert the login was successful
        self.assertEqual(response['status'], 200)
        self.assertIn('token', response['data'])
        self.assertEqual(response['data']['user_id'], user_data["_id"])

        # Print test result
        print("Test 'test_login_user' passed successfully.")

if __name__ == '__main__':
    unittest.main()