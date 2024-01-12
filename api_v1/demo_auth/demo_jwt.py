from users.schemas import UserSchema
from jwt.exceptions import InvalidTokenError
from auth import utils as auth_utils
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel

router = APIRouter(prefix="/jwt", tags=["JWT"])
# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo_auth/jwt/login/",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


barney = UserSchema(
    username="Barney",
    password=auth_utils.hash_pass("qwerty"),
    email="barney2016@yandex.ru",
)
dazdik = UserSchema(
    username="Dazdik",
    password=auth_utils.hash_pass("asdfg"),
)

users_db: dict[str, UserSchema] = {barney.username: barney, dazdik.username: dazdik}


def check_user(username: str = Form(), password: str = Form()):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
    )
    if not (user := users_db.get(username)):
        raise credentials_exc
    if not auth_utils.check_pass(password=password, hashed_password=user.password):
        raise credentials_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )
    return user


def get_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_utils.decoded_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )
    return payload


def get_current_user(
    payload: dict = Depends(get_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )


def get_current_active_user(user: UserSchema = Depends(get_current_user)):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )
    return user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(check_user)):
    jwt_payload = {"sub": user.username, "username": user.username, "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_payload),
    user: UserSchema = Depends(get_current_active_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
