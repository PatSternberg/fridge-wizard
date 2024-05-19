import unittest
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class TestCreateUser(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['users']

    def tearDown(self):
        # Clean up MongoDB
        self.db.drop_collection('users')
        self.client.close()

    def test_signup_user(self):
        # define the creation of an user
        user_data = {
            "_id": "someId",
            "username": "someUsername1",
            "password": "somePassword1",
            "email" : "someEmail1"
        }

        # add the fridge document to the DB
        self.collection.insert_one(user_data)

        # retrieve the fridge document from DB
        retrieved_document = self.collection.find_one({"_id": "someId"})

        # Assert that the retrieved document matches the test document
        self.assertEqual(retrieved_document["_id"], user_data["_id"])
        self.assertEqual(retrieved_document["username"], user_data["username"])
        self.assertEqual(retrieved_document["password"], user_data["password"])
        # retrieved_document["email"] = "diffemail@abc.com"
        self.assertEqual(retrieved_document["email"], user_data["email"])

        
        # Print test result
        print("Test 'test_signup_user' passed successfully.")

if __name__ == '__main__':
    unittest.main()