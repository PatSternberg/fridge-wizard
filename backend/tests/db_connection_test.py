import unittest
from pymongo import MongoClient

class TestDBConnection(unittest.TestCase):
    def setUp(self):
        # establish connection to MongoDB
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['fridge_hero_test']

    def tearDown(self):
        # close connection to MongoDB
        self.client.close()

    def test_Mongo_connection(self):
        try:
            # replace these values with test MongoDB details
            client = MongoClient('mongodb://localhost:27017/')
            db = client['fridge_hero_test']

            # execute a ping command to check connection
            db.command('ping')

            client.close()

        except Exception as e:
            print("Error:", e)
            self.fail("Connection to MongoDB failed.")

if __name__ == "__main__":
    unittest.main()