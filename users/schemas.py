from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: str | None = None
    active: bool = True
