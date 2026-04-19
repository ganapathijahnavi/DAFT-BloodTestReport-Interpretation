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
from .interpretation import (
    extract_abnormal_findings,
    detect_conditions
)
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


# ============================
# 🔥 CLINICAL INSIGHTS
# ============================
def generate_clinical_insights(abnormal_findings):
    insights = []

    for item in abnormal_findings:
        if "Haemoglobin" in item:
            insights.append("Low haemoglobin indicates anemia and reduced oxygen supply")

        if "MCV" in item:
            insights.append("Low MCV suggests microcytic anemia due to iron deficiency")

        if "MCHC" in item:
            insights.append("Low MCHC indicates reduced hemoglobin concentration")

        if "ESR" in item:
            insights.append("High ESR suggests inflammation or infection")

        if "Glucose" in item:
            insights.append("High glucose indicates risk of diabetes")

        if "TSH" in item:
            insights.append("Abnormal TSH indicates thyroid dysfunction")

    return "\n".join(insights)


# ============================
# DATABASE
# ============================
@app.on_event("startup")
def startup_event():
    connect_db()


@app.on_event("shutdown")
def shutdown_event():
    close_database()


def _get_collection():
    return get_database()["test_results"]


# ============================
# AUTH
# ============================
async def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    user_id = extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id


# ============================
# AUTH ENDPOINTS
# ============================
@app.post("/auth/signup", response_model=Token)
async def signup(user: UserSignUp):
    result = create_user(user.email, user.password, user.full_name)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    token = create_access_token(data={"sub": result["user_id"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": result["user_id"],
            "email": user.email,
            "full_name": user.full_name
        }
    }


@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    result = verify_user_credentials(user.email, user.password)

    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])

    token = create_access_token(data={"sub": result["user"]["id"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": result["user"]
    }


@app.get("/auth/me", response_model=UserResponse)
async def me(user_id: str = Depends(get_current_user)):
    user = get_user_by_id(user_id)
    return user


# ============================
# 🔥 MAIN PIPELINE
# ============================
@app.post("/upload-ocr")
async def upload_ocr(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    collection = _get_collection()

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_file(file_path)

    if not text.strip():
        return {"output": "No readable data"}

    # 🔥 parsing
    lab_values = parse_lab_values(text)

    # 🔥 abnormal
    abnormal = extract_abnormal_findings(lab_values)

    # 🔥 conditions
    conditions = detect_conditions(abnormal)

    # 🔥 insights
    insights = generate_clinical_insights(abnormal)

    # 🔥 strong input
    model_input = f"""
Abnormal Findings:
{', '.join(abnormal)}
Possible Conditions:
{', '.join(conditions)}
Clinical Insights:
{insights}
Full Report:
{text[:1200]}
"""

    output = run_medical_model(model_input)

    doc = {
        "user_id": user_id,
        "file_name": file.filename,
        "uploaded_at": datetime.utcnow(),
        "lab_values": lab_values,
        "abnormal_findings": abnormal,
        "conditions": conditions,
        "clinical_insights": insights,
        "medical_interpretation": output,
        "chat_history": []
    }

    result = collection.insert_one(doc)

    os.remove(file_path)

    return {
        "output": output,
        "test_result_id": str(result.inserted_id),
        "conditions": conditions,
        "abnormal_findings": abnormal
    }


# ============================
# TEST RESULTS
# ============================
@app.get("/test-results")
async def get_results(user_id: str = Depends(get_current_user)):
    collection = _get_collection()

    results = list(collection.find({"user_id": user_id}).sort("uploaded_at", -1))

    for r in results:
        r["_id"] = str(r["_id"])

    return {"results": results}


@app.get("/test-results/{test_id}")
async def get_result(test_id: str, user_id: str = Depends(get_current_user)):
    collection = _get_collection()

    result = collection.find_one({
        "_id": ObjectId(test_id),
        "user_id": user_id
    })

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    result["_id"] = str(result["_id"])
    return result


# ============================
# CHAT
# ============================
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, user_id: str = Depends(get_current_user)):
    collection = _get_collection()

    result = collection.find_one({
        "_id": ObjectId(chat_request.test_result_id),
        "user_id": user_id
    })

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    context = f"""
Abnormal Findings:
{', '.join(result.get('abnormal_findings', []))}
Conditions:
{', '.join(result.get('conditions', []))}
Insights:
{result.get('clinical_insights', '')}
"""

    answer = chat_about_report(context, chat_request.message)

    entry = {
        "question": chat_request.message,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }

    collection.update_one(
        {"_id": ObjectId(chat_request.test_result_id)},
        {"$push": {"chat_history": entry}}
    )

    return ChatResponse(
        question=chat_request.message,
        answer=answer,
        timestamp=entry["timestamp"]
    )


@app.get("/chat-history/{test_id}")
async def chat_history(test_id: str, user_id: str = Depends(get_current_user)):
    collection = _get_collection()

    result = collection.find_one({
        "_id": ObjectId(test_id),
        "user_id": user_id
    })

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"chat_history": result.get("chat_history", [])}
