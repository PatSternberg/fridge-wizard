# file: utils.py
# Contains function for creating database connection with pymongo

# file: utils.py
# Contains function for creating database connection with pymongo

from pymongo import MongoClient

def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                        )
    db_handle = client[db_name]
    return db_handle, client