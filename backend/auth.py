"""
Authentication utilities for JWT tokens and password hashing
Safe for bcrypt + passlib in Docker / Hugging Face Spaces
"""

from datetime import datetime, timedelta
from typing import Optional
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# ============================
# JWT CONFIGURATION
# ============================
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# ============================
# PASSWORD HASHING (bcrypt-safe)
# ============================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_BCRYPT_BYTES = 72


def _normalize_password(password: str) -> str:
    """
    bcrypt only supports 72 bytes.
    We truncate safely to avoid runtime crashes.
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        password_bytes = password_bytes[:MAX_BCRYPT_BYTES]
    return password_bytes.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (safe)"""
    safe_password = _normalize_password(password)
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash (safe)"""
    safe_password = _normalize_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)


# ============================
# JWT UTILITIES
# ============================
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """Extract user_id from JWT token"""
    payload = decode_token(token)
    if payload:
        return payload.get("sub")
    return None
