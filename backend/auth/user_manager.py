# file: backend/auth/user_manager.py
from utility.db_handler import DBHandler

def get_user_by_credentials(username, password):
    db_handler = DBHandler()
    db, client = db_handler.get_db_handle(db_name='fridge-hero', host='localhost', port=27017, username='', password='')
    users_collection = db['users']
    user = users_collection.find_one({'username': username, 'password': password})
    client.close()
    return user