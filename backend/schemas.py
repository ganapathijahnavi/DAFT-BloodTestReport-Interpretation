from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ============ USER SCHEMAS ============

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str = None
    email: str
    full_name: str
    created_at: datetime = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# ============ TEST RESULT SCHEMAS ============

class LabValue(BaseModel):
    test_name: str
    value: float
    unit: Optional[str] = None
    status: str  # NORMAL, HIGH, LOW


class MedicalResponse(BaseModel):
    extracted_text: str
    model_output: Optional[str] = None
    lab_values: Optional[dict] = None


class TestResult(BaseModel):
    user_id: str
    file_name: str
    uploaded_at: datetime
    extracted_text: str
    lab_values: dict
    abnormal_findings: List[str]
    medical_interpretation: str
    status: str = "completed"


class TestResultResponse(BaseModel):
    id: str = None
    file_name: str
    uploaded_at: datetime
    abnormal_findings: List[str]
    medical_interpretation: str


# ============ CHAT SCHEMAS ============

class ChatRequest(BaseModel):
    test_result_id: str
    message: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    timestamp: datetime

# uvicorn main:app --reload