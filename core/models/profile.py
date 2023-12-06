from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from .base import Base
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profiles"
    first_name: Mapped[str | None] = mapped_column(String(25))
    last_name: Mapped[str | None] = mapped_column(String(30))
    bio: Mapped[str | None]
