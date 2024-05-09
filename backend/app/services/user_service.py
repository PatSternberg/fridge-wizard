import requests
import json

BASE_URL = "http://127.0.0.1:8000/"

def create_user(data): # function to send a post request to create a new user 

    url = f"{BASE_URL}/app/views/create_user_view/"
    response = requests.post(url, json=data)
    return response

def get_user(user_id):
    url = f"{BASE_URL}/app/views/get_user_view"  
    response = requests.get(url)
    return response

def signup_user(username, email, password):
    url = f"{BASE_URL}backened/controllers/users/signup"
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response
    
