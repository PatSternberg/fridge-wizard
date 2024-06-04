import unittest
import os
import django
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class TestFridgeDocuments(unittest.TestCase):
    def setUp(self):
        # Establish connection to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('TEST_DB_NAME')]
        self.collection = self.db['fridges']

    def tearDown(self):
        # Clean up MongoDB
        self.db.drop_collection('fridges')
        self.client.close()

    def test_add_fridge_document(self):
        # Define the fridge document data
        fridge_data = {
            "_id": "someId",
            "storedItems": {
                "someCategory": {
                    "someItem1": "someExpiry1",
                    "someItem2": "someExpiry2"
                },
                "someCategory2": {
                    "someItem3": "someExpiry3",
                    "someItem4": "someExpiry4"
                }
            },
            "user_id": "someUsersId"
        }

        # Add the fridge document to MongoDB
        self.collection.insert_one(fridge_data)

        # Retrieve the fridge document from MongoDB
        retrieved_document = self.collection.find_one({"_id": "someId"})

        # Assert that the retrieved document matches the test document
        self.assertEqual(retrieved_document["storedItems"], fridge_data["storedItems"])
        self.assertEqual(retrieved_document["user_id"], fridge_data["user_id"])
        
        # Print test result
        print("Test 'test_add_fridge_document' passed successfully.")

if __name__ == '__main__':
    unittest.main()