from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

ALGORITHM = "HS256"

# In production this should be a strong random secret key
SECRET_KEY = "super_secret_aegis_key_for_beta"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=365) # Long lived tokens for agents for now
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username

def get_current_admin(current_user: str = Depends(get_current_user)):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

def get_current_agent(current_user: str = Depends(get_current_user)):
    # Very simple for beta: assume if it's a digit it's an agent ID
    if not current_user.isdigit():
        raise HTTPException(status_code=403, detail="Not a valid agent token")
    return int(current_user)
