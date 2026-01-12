"""
User management service for handling user operations
"""

from bson import ObjectId
import re
import dns.resolver
from datetime import datetime

from .database import get_database
from .auth import hash_password, verify_password


def _get_users_collection():
    db = get_database()
    return db["users"]


def validate_email_domain(email: str) -> dict:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return {"valid": False, "message": "Invalid email format"}

    try:
        domain = email.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
        return {"valid": True, "message": "Email domain is valid"}
    except Exception:
        # Do not block signup due to DNS/network issues
        return {"valid": True, "message": "Email domain could not be verified"}


def create_user(email: str, password: str, full_name: str) -> dict:
    users_collection = _get_users_collection()

    validation_result = validate_email_domain(email)
    if not validation_result["valid"]:
        return {"success": False, "message": validation_result["message"]}

    if users_collection.find_one({"email": email}):
        return {"success": False, "message": "Email already registered"}

    hashed_password = hash_password(password)

    user_data = {
        "email": email,
        "password": hashed_password,
        "full_name": full_name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = users_collection.insert_one(user_data)

    return {
        "success": True,
        "user_id": str(result.inserted_id),
        "message": "User created successfully"
    }


def get_user_by_email(email: str) -> dict | None:
    users_collection = _get_users_collection()
    user = users_collection.find_one({"email": email})

    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
        "full_name": user["full_name"],
        "created_at": user.get("created_at"),
    }


def get_user_by_id(user_id: str) -> dict | None:
    users_collection = _get_users_collection()
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None

        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "created_at": user.get("created_at"),
        }
    except Exception:
        return None


def verify_user_credentials(email: str, password: str) -> dict:
    user = get_user_by_email(email)

    if not user:
        return {"success": False, "message": "Invalid email or password"}

    if not verify_password(password, user["password"]):
        return {"success": False, "message": "Invalid email or password"}

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
        }
    }
