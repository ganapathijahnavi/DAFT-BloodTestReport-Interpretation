# backend/main.py
import os
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from .ocr import extract_text_from_file
from .model import run_medical_model, chat_about_report
from .lab_parser import parse_lab_values
from .interpretation import extract_abnormal_findings
from .schemas import (
    UserSignUp,
    UserLogin,
    Token,
    UserResponse,
    ChatRequest,
    ChatResponse
)
from .auth import create_access_token, extract_user_id_from_token
from .user_service import create_user, verify_user_credentials, get_user_by_id
from .database import connect_db, close_database, get_database


# ----------------------------
# APP SETUP
# ----------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Medical Report Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# DATABASE LIFECYCLE
# ----------------------------
@app.on_event("startup")
def startup_event():
    connect_db()


@app.on_event("shutdown")
def shutdown_event():
    close_database()


# ----------------------------
# DB COLLECTION HELPERS
# ----------------------------
def _get_test_results_collection():
    db = get_database()
    return db["test_results"]


# ----------------------------
# AUTH DEPENDENCY
# ----------------------------
async def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    user_id = extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_id


# ============================
# AUTH ENDPOINTS
# ============================
@app.post("/auth/signup", response_model=Token)
async def signup(user_data: UserSignUp):
    result = create_user(
        user_data.email,
        user_data.password,
        user_data.full_name
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    access_token = create_access_token(data={"sub": result["user_id"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": result["user_id"],
            "email": user_data.email,
            "full_name": user_data.full_name
        }
    }


@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    result = verify_user_credentials(
        user_data.email,
        user_data.password
    )

    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])

    user = result["user"]
    access_token = create_access_token(data={"sub": user["id"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(user_id: str = Depends(get_current_user)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============================
# UPLOAD & ANALYSIS
# ============================
@app.post("/upload-ocr")
async def upload_ocr(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    collection = _get_test_results_collection()

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_file(file_path)

    if not extracted_text.strip():
        os.remove(file_path)
        return {"output": "No readable medical data found in the document."}

    lab_values = parse_lab_values(extracted_text)
    abnormal_findings = extract_abnormal_findings(lab_values)
    model_output = run_medical_model(extracted_text)

    test_result = {
        "user_id": user_id,
        "file_name": file.filename,
        "uploaded_at": datetime.utcnow(),
        "extracted_text": extracted_text,
        "lab_values": lab_values,
        "abnormal_findings": abnormal_findings,
        "medical_interpretation": model_output,
        "status": "completed"
    }

    result = collection.insert_one(test_result)
    os.remove(file_path)

    return {
        "output": model_output,
        "test_result_id": str(result.inserted_id),
        "lab_values": lab_values,
        "abnormal_findings": abnormal_findings
    }


# ============================
# TEST RESULTS
# ============================
@app.get("/test-results")
async def get_user_test_results(
    user_id: str = Depends(get_current_user),
    limit: int = 50
):
    collection = _get_test_results_collection()

    results = list(
        collection.find({"user_id": user_id})
        .sort("uploaded_at", -1)
        .limit(limit)
    )

    for r in results:
        r["_id"] = str(r["_id"])

    return {"total": len(results), "results": results}


@app.get("/test-results/{test_id}")
async def get_test_result(
    test_id: str,
    user_id: str = Depends(get_current_user)
):
    collection = _get_test_results_collection()

    try:
        result = collection.find_one({
            "_id": ObjectId(test_id),
            "user_id": user_id
        })

        if not result:
            raise HTTPException(status_code=404, detail="Test result not found")

        result["_id"] = str(result["_id"])
        return result

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")


# ============================
# CHAT
# ============================
@app.post("/chat", response_model=ChatResponse)
async def chat_with_report(
    chat_request: ChatRequest,
    user_id: str = Depends(get_current_user)
):
    collection = _get_test_results_collection()

    result = collection.find_one({
        "_id": ObjectId(chat_request.test_result_id),
        "user_id": user_id
    })

    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")

    report_context = f"""
Extracted Text: {result.get('extracted_text', '')}
Lab Values: {result.get('lab_values', {})}
Abnormal Findings: {', '.join(result.get('abnormal_findings', []))}
Medical Interpretation: {result.get('medical_interpretation', '')}
"""

    answer = chat_about_report(report_context, chat_request.message)

    chat_entry = {
        "question": chat_request.message,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }

    collection.update_one(
        {"_id": ObjectId(chat_request.test_result_id)},
        {"$push": {"chat_history": chat_entry}}
    )

    return ChatResponse(
        question=chat_request.message,
        answer=answer,
        timestamp=chat_entry["timestamp"]
    )


@app.get("/chat-history/{test_id}")
async def get_chat_history(
    test_id: str,
    user_id: str = Depends(get_current_user)
):
    collection = _get_test_results_collection()

    result = collection.find_one({
        "_id": ObjectId(test_id),
        "user_id": user_id
    })

    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")

    return {"chat_history": result.get("chat_history", [])}
