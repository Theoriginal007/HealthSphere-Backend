# db/mongodb.py

from pymongo import MongoClient, errors
import os

# MongoDB URI from environment variable (preferably not hardcoded)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/healthsphere')

# Initialize the MongoDB client with error handling
try:
    client = MongoClient(MONGO_URI)
    db = client['healthsphere']
    print("Connected to MongoDB")
except errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    db = None

# Example collection
users_collection = db['users'] if db else None

# Insert a new user into MongoDB
def add_user(user_data: dict):
    if db:
        try:
            result = users_collection.insert_one(user_data)
            return result.inserted_id
        except errors.PyMongoError as e:
            print(f"Error inserting user: {e}")
            return None
    return None

# Get a user by email from MongoDB
def get_user_by_email(email: str):
    if db:
        try:
            return users_collection.find_one({"email": email})
        except errors.PyMongoError as e:
            print(f"Error fetching user: {e}")
            return None
    return None
