import unittest
import os
import django
from dotenv import load_dotenv
from auth.auth import generate_token
from bson.objectid import ObjectId
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['users']

    def tearDown(self):
        # Clean up MongoDB
        self.db.drop_collection('users')
        self.client.close()

    def test_generate_token(self):
        user_id = str(ObjectId())

        # Generate a token using ObjectID
        token = generate_token(user_id)

        # Assert a string token was returned
        self.assertIsInstance(token, str)

        # Print test result
        print("Test 'test_generate token' passed successfully.")
