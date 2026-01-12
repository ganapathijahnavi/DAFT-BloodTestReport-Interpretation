"""
Database configuration and connection for MongoDB
Safe for Hugging Face Spaces + FastAPI + MongoDB Atlas
"""

import os
from typing import Optional

from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

# ============================
# ENVIRONMENT VARIABLES
# ============================
MONGODB_URL: Optional[str] = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "medical_reports_db")

# ============================
# GLOBAL DB OBJECTS
# ============================
client: Optional[MongoClient] = None
database = None
users_collection = None
test_results_collection = None


# ============================
# CONNECT TO DATABASE
# ============================
def connect_db():
    """
    Initialize MongoDB connection.
    Called once during FastAPI startup.
    """
    global client, database, users_collection, test_results_collection

    if not MONGODB_URL:
        raise RuntimeError("❌ MONGODB_URL is not set in environment variables")

    # Prevent reconnecting
    if client is not None:
        return

    try:
        client = MongoClient(
            MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
        )

        # Force connection check
        client.admin.command("ping")

        database = client[DB_NAME]

        users_collection = database["users"]
        test_results_collection = database["test_results"]

        # Create indexes (non-fatal)
        try:
            users_collection.create_index("email", unique=True)
            test_results_collection.create_index("user_id")
            test_results_collection.create_index("timestamp", background=True)
        except Exception as index_error:
            print(f"⚠️ Index creation skipped: {index_error}")

        print("✅ MongoDB connected successfully")

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise RuntimeError("MongoDB connection failed")


# ============================
# GET DATABASE
# ============================
def get_database():
    """
    Get database instance (after connect_db).
    """
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_db() first.")
    return database


# ============================
# CLOSE DATABASE
# ============================
def close_database():
    """
    Close MongoDB connection gracefully.
    """
    global client
    if client:
        client.close()
        client = None
        print("🔌 MongoDB connection closed")
