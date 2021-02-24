import pymongo
import hashlib, uuid
import copy
from pprint import pprint

client = pymongo.MongoClient("mongodb+srv://admin:admin@imdb.ewvcu.mongodb.net/IMDB?retryWrites=true&w=majority")
database_name = "IMDB"

def get_collection(collection_name):
    imdb_db = client[database_name]
    return imdb_db[collection_name]

def encrypt_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    return hashed_password, salt

def encrypt_password_and_add_SALT(_users_data):
    copied_data = copy.deepcopy(_users_data)
    for user_data in copied_data:
        hashed_password, salt = encrypt_password(user_data["password"])
        user_data["password"] = hashed_password
        user_data["SALT"] = salt
    return copied_data

def insert_example():
    user_collection = get_collection("user")
    users_data = [
        { 
            "name": "François", 
            "lastname": "HOLLANDE",
            "mail": "francois.hollande@gmail.com",
            "login": "FrantzH",
            "password": "root",
            "SALT": "",
        },
        { 
            "name": "Marie", 
            "lastname": "CURIE",
            "mail": "marie.curie@gmail.com",
            "login": "MarieCDu93",
            "password": "root",
            "SALT": "",
        },
    ]
    # Hash passwords
    users_data_with_hashed_passwords_and_SALTs = encrypt_password_and_add_SALT(users_data)

    # Insert into DB
    x = user_collection.insert_many(users_data_with_hashed_passwords_and_SALTs)

    print(x.inserted_ids)

# insert_example()

# db = client.get_default_database()
# pprint(db.command("serverStatus"))

print("This script is deprecated. Rather use db_utils.py with mongoengine.")