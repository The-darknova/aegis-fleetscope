from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str, token_type: str = "user", version: int | None = None, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        # Default to short lived access tokens for users, long lived for agents
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    if version is not None:
        to_encode["version"] = version
        
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str, version: int, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh", "version": version}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return payload

def get_current_admin(payload: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.get("type") != "user":
        raise HTTPException(status_code=403, detail="Invalid token type")
        
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not user.is_active or user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    if payload.get("version") != user.token_version:
        raise HTTPException(status_code=401, detail="Token has been invalidated")
        
    return user

def get_current_agent(payload: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models.host import Host
    
    if payload.get("type") != "agent":
        raise HTTPException(status_code=403, detail="Not a valid agent token")
        
    sub = payload.get("sub")
    if not sub or not sub.isdigit():
        raise HTTPException(status_code=403, detail="Invalid agent token subject")
        
    host = db.query(Host).filter(Host.id == int(sub)).first()
    if not host or not host.is_active:
        raise HTTPException(status_code=403, detail="Agent not found or inactive")
        
    return host.id

def get_authenticated_agent(payload: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models.host import Host
    
    if payload.get("type") != "agent":
        raise HTTPException(status_code=403, detail="Not a valid agent token")
        
    sub = payload.get("sub")
    if not sub or not sub.isdigit():
        raise HTTPException(status_code=403, detail="Invalid agent token subject")
        
    host = db.query(Host).filter(Host.id == int(sub)).first()
    if not host or not host.is_active:
        raise HTTPException(status_code=403, detail="Agent not found or inactive")
        
    if not host.agent_key:
        raise HTTPException(status_code=403, detail="Agent key not initialized")
        
    return host
