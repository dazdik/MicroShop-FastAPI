from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"  # указать путь к файлу с БД
    # db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"  # указание абсолютного пути к БД
    db_echo: bool = True  # поменять на False


settings = Settings()
