from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlmodel import Session, select
from src.database import get_session
from src.models.tables import User
from src.config import settings
from src.security import (
    verify_password,
    create_access_token,
    get_current_user,
    get_current_admin_user,
)

auth_router = APIRouter()

@auth_router.post("/token", tags=['Auth'])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict"
    )
    return response

@auth_router.get("/profile", tags=['Auth'])
def profile(my_user: Annotated[dict, Depends(get_current_user)]):
    return my_user

@auth_router.get('/dashboard', tags=['Auth'])
def dashboard(admin_user: Annotated[dict, Depends(get_current_admin_user)]):
    return {"message": f"Welcome to the admin dashboard, {admin_user['username']}!", "user_data": admin_user}