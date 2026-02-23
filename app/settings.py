# app/settings.py – FIXED for Python 3.9
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from typing import Optional   # ← Add this import

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="allow"
    )

    SECRET_KEY: str
    DATABASE_URL: Optional[str] = None   # ← Use Optional[str] instead of str | None
    API_KEY: Optional[str] = None        # ← Same here

settings = Settings()