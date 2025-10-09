from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from jose import jwt  # type: ignore

auth_router = APIRouter()

# Volvemos a usar contraseñas en texto plano para simplificar.
users = {
    "reich": {"username": "reich", "email": "reich@g.com", "password": "123456", "role": "admin"},
    "will": {"username": "will", "email": "will@g.com", "password": "fakepass", "role": "user"},
}

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token_from_cookie(access_token: Annotated[str | None, Cookie()] = None) -> dict:
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        data = jwt.decode(access_token, "my-secret", algorithms=["HS256"])
        user = users.get(data["username"])
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        user_data = user.copy() # pyright: ignore[reportOptionalMemberAccess]
        user_data.pop("password", None)
        return user_data
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_admin_user(current_user: Annotated[dict, Depends(decode_token_from_cookie)]):
    """Depends to verify if the user is an administrador."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

### Authentication Endpoints ###

@auth_router.post("/token", tags=['Auth'])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password")
    
    token_payload = {"username": user["username"], "role": user["role"]}
    token = encode_token(token_payload)

    # Stablish token as secure cookie
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # ¡Importante para la seguridad!
        samesite="strict"
    )
    return response

@auth_router.get("/profile", tags=['Auth'])
def profile(my_user: Annotated[dict, Depends(decode_token_from_cookie)]):
    return my_user

@auth_router.get('/dashboard', tags=['Auth'])
def dashboard(admin_user: Annotated[dict, Depends(get_current_admin_user)]):
    return {"message": f"Welcome to the admin dashboard, {admin_user['username']}!", "user_data": admin_user}