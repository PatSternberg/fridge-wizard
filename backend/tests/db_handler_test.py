# file: ./tests/db_handler_test.py
import unittest
import os
import django
from pymongo import MongoClient
from utility.db_handler import DBHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class TestDBHandler(unittest.TestCase):
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