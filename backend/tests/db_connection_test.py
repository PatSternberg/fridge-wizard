import unittest
import os
from dotenv import load_dotenv
from pymongo import MongoClient

class TestDBConnection(unittest.TestCase):
    def setUp(self):
        # establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]

    def tearDown(self):
        # close connection to MongoDB
        self.client.close()

    def test_Mongo_connection(self):
        try:
            # replace these values with test MongoDB details
            client = MongoClient(os.getenv('MONGODB_URI'))
            db = client[os.getenv('TEST_DB_NAME')]

            # execute a ping command to check connection
            db.command('ping')

            client.close()

        except Exception as e:
            print("Error:", e)
            self.fail("Connection to MongoDB failed.")

if __name__ == "__main__":
    unittest.main()