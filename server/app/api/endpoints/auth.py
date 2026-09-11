from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, verify_password, get_current_admin
from app.db.session import get_db
from app.models.user import User
import jwt
from app.core.config import settings

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password) or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(subject=user.username, version=user.token_version)
    refresh_token = create_refresh_token(subject=user.username, version=user.token_version)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(req: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(req.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        username = payload.get("sub")
        token_version = payload.get("version")
        
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
            
        if user.token_version != token_version:
            raise HTTPException(status_code=401, detail="Refresh token has been invalidated")
            
        new_access_token = create_access_token(subject=user.username, version=user.token_version)
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    # Invalidate all current tokens by incrementing the token_version
    current_user.token_version += 1
    db.commit()
    return {"message": "Successfully logged out across all devices"}

