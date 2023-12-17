import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo_auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
async def basic_auth_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    return {
        "message": "Hi, user!",
        "username": credentials.username,
        "password": credentials.password,
    }


username_to_pass = {"admin": "admin", "dazd": "password"}


def get_auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_pass = username_to_pass.get(credentials.username)
    if correct_pass is None:
        raise unauth_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"), correct_pass.encode("utf-8")
    ):
        raise unauth_exc
    return credentials.username


@router.get("/basic-auth-username/")
async def basic_auth_credentials(username: str = Depends(get_auth_user)):
    return {"message": f"Hi, {username}", "username": username}
