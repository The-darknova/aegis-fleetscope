from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    # In a real app, verify against DB. For beta, hardcode a simple admin check
    if req.username == "admin" and req.password == "admin":
        token = create_access_token(subject="admin")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
