# file: views.py
from django.http import HttpResponse
from pymongo import MongoClient
from .services.user_service import create_user, get_user
from django.shortcuts import render

# Create your views here.

# Example of importing the database connection logic and creating
# a database connection

#from .utils import get_db_handle

def user_view(request):                 #http request from client
    # connect to mongo db
    client = MongoClient('mongodb://localhost:27017')
    db = client['fridge_hero']
    collection = db['users']

    # testing if i can insert a user to the db
    user_data = {
        'id': '011',
        'username': 'kevin',
        'email': 'kevin@gmail.com',
        'password': 'pass123'
    }
    collection.insert_one(user_data)

    return HttpResponse('user inserted succesfully')

def my_mongo_view():
    # Your MongoDB connection details
    host = 'localhost'
    port = 27017
    username = 'admin'
    password = 'admin'
    db_name = 'fridge_hero'

    # Get the database handle and client
    db_handle, client = get_db_handle(db_name, host, port, username, password)

    # Now you can use db_handle to interact with your MongoDB database
    # For example:
    collection = db_handle['my_collection']
    result = collection.find_one({'some_key': 'some_value'})
    
    # Don't forget to close the client when you're done
    
    client.close()

