# db/postgres.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import os

# Set up database URL from environment variables or fallback to a hardcoded URL (not recommended for production)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

# Set up the SQLAlchemy engine with connection pooling
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)

# SessionLocal binds to the engine and can be used for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()

# Context manager for managing database sessions in a safe and reusable way
@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example model: User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Create all tables in the database (run only once or during migrations)
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")

# Example function for adding a user to the database
def add_user(db: Session, name: str, email: str, password: str):
    new_user = User(name=name, email=email, hashed_password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Example function for querying users
def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        print(f"Error fetching user by email: {e}")
        return None

# Running the creation of tables (only required in the initial setup or migrations)
if __name__ == "__main__":
    create_tables()
