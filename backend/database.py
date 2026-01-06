"""
Database configuration and connection for MongoDB
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection string
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "medical_reports_db"

# Initialize MongoDB client
client = MongoClient(MONGODB_URL)
database = client[DB_NAME]

# Collections
users_collection = database["users"]
test_results_collection = database["test_results"]

# Create indexes for better performance
users_collection.create_index("email", unique=True)
test_results_collection.create_index("user_id")
test_results_collection.create_index("timestamp", background=True)


def get_database():
    """Get database instance"""
    return database


def close_database():
    """Close MongoDB connection"""
    client.close()
