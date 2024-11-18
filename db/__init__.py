# db/__init__.py

# Initialize the PostgreSQL connection and functions
from .postgres import engine, SessionLocal, get_db, add_user, get_user_by_email

# Initialize the MongoDB connection and functions
from .mongodb import db, users_collection, add_user as add_mongo_user, get_user_by_email as get_mongo_user_by_email
