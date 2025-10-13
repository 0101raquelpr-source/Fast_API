import hashlib
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import Depends, HTTPException, status, Cookie
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from src.database import get_session
from src.models.tables import User
from src.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a password first with SHA-256 and then with bcrypt.
    This avoids bcrypt's 72-byte limit by always hashing a 64-character hex string.
    """
    sha256_hex = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256_hex)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password by applying the same SHA-256 + bcrypt logic.
    """
    sha256_hex = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256_hex, hashed_password)

# JWT Token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str, session: Session) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Union[str, None] = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        
        user_data = user.model_dump()
        user_data.pop("password", None)
        return user_data
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(access_token: Annotated[Union[str, None], Cookie()] = None, session: Session = Depends(get_session)) -> dict:
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return decode_token(access_token, session)

def get_current_admin_user(current_user: Annotated[dict, Depends(get_current_user)]):
    """Depends to verify if the user is an administrador."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user