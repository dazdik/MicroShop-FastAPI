import secrets
import uuid
from time import time
from typing import Any

from fastapi import (APIRouter, Cookie, Depends, Header, HTTPException,
                     Response, status)
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
static_auth_token_to_username = {
    "39a6c9f2eff5aa9ded107e02bc": "admin",
    "9e30ac5a588057b526aeb038164b31f518894c": "dazd",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


def get_auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
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


@router.get("/some_http_headers_auth/")
async def some_http_headers_auth(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {"message": f"Hi, {username}", "username": username}


COOKIES: dict[str, dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = "web-app-session-id"


def get_session_data(session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return COOKIES[session_id]


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post("/login-cookie/")
async def demo_login_cookie(
    response: Response,
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    return {"message": "everything ok"}


@router.get("/check-cookie/")
async def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    return {"username": username, **user_session_data}


@router.get("/logout-cookie/")
async def demo_auth_check_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"message": f"Bye, {username}"}
