# file: backend/backend/tests/db_connection_test.py
import unittest
import os
import django
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class TestMongoDBConnection(unittest.TestCase):
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


class TestMongoTestDBConnection(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()