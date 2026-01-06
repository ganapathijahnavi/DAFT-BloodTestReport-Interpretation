"""
User management service for handling user operations
"""
from bson import ObjectId
from database import users_collection
from auth import hash_password, verify_password
from schemas import UserResponse
import dns.resolver
import re


def validate_email_domain(email: str) -> dict:
    """Validate if email domain has valid MX records"""
    
    # Basic format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return {"valid": False, "message": "Invalid email format"}
    
    try:
        # Extract domain from email
        domain = email.split('@')[1]
        
        # Check for MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        
        if mx_records:
            return {"valid": True, "message": "Email domain is valid"}
        else:
            return {"valid": False, "message": "Email domain has no mail servers"}
            
    except dns.resolver.NXDOMAIN:
        return {"valid": False, "message": "Email domain does not exist"}
    except dns.resolver.NoAnswer:
        return {"valid": False, "message": "Email domain has no MX records"}
    except dns.resolver.NoNameservers:
        return {"valid": False, "message": "No nameservers available for domain"}
    except Exception as e:
        # If DNS check fails, allow signup (network issues shouldn't block users)
        return {"valid": True, "message": "Could not verify email domain, proceeding anyway"}


def create_user(email: str, password: str, full_name: str) -> dict:
    """Create a new user"""
    
    # Validate email domain
    validation_result = validate_email_domain(email)
    if not validation_result["valid"]:
        return {"success": False, "message": validation_result["message"]}
    
    # Check if user already exists
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return {"success": False, "message": "Email already registered"}
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Create user document
    user_data = {
        "email": email,
        "password": hashed_password,
        "full_name": full_name,
        "created_at": __import__("datetime").datetime.utcnow(),
        "updated_at": __import__("datetime").datetime.utcnow()
    }
    
    # Insert into database
    result = users_collection.insert_one(user_data)
    
    return {
        "success": True,
        "user_id": str(result.inserted_id),
        "message": "User created successfully"
    }


def get_user_by_email(email: str) -> dict:
    """Get user by email"""
    user = users_collection.find_one({"email": email})
    
    if not user:
        return None
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
        "full_name": user["full_name"],
        "created_at": user.get("created_at")
    }


def get_user_by_id(user_id: str) -> dict:
    """Get user by ID"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return None
        
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "created_at": user.get("created_at")
        }
    except:
        return None


def verify_user_credentials(email: str, password: str) -> dict:
    """Verify user credentials and return user if valid"""
    user = get_user_by_email(email)
    
    if not user:
        return {"success": False, "message": "Invalid email or password"}
    
    if not verify_password(password, user["password"]):
        return {"success": False, "message": "Invalid email or password"}
    
    # Return user without password
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    }
