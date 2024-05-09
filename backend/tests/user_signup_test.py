import unittest
from pymongo import MongoClient

class TestCreateUser(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['fridge_hero_testing']
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