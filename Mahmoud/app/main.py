from app.cache import get_cache, set_cache, delete_cache
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.auth import hash_password, verify_password, create_access_token, decode_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Online Examination System")

users_db = {}


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "student"


class LoginRequest(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    username = payload.get("sub")

    if username is None or username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")

    return users_db[username]


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@app.post("/auth/register")
def register(data: RegisterRequest):
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_db[data.username] = {
        "username": data.username,
        "password": hash_password(data.password),
        "role": data.role
    }

    return {"message": "User registered successfully"}


@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "role": current_user["role"]
    }


@app.post("/exams")
def create_exam(current_user: dict = Depends(require_admin)):

    delete_cache("exams")

    return {
        "message": "Exam created successfully",
        "cache": "cleared"
    }


@app.get("/exams")
def get_exams():

    cached_data = get_cache("exams")

    if cached_data:
        return {
            "source": "cache",
            "data": cached_data
        }

    exams = [
        {"id": 1, "title": "Python Exam"},
        {"id": 2, "title": "Database Exam"}
    ]

    set_cache("exams", exams)

    return {
        "source": "database",
        "data": exams
    }



#http://127.0.0.1:8000/docs
#python -m uvicorn app.main:app --reload
#C:\Users\Ahamed Abo Elnasr\Desktop\online_exam_system\app