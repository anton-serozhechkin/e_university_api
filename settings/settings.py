import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    # DATABASE SETTINGS
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PASSWORD: str = Field(default='postgres')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DSN: PostgresDsn = \
        f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/foobar'

    # BACK-END SETTINGS
    TOKEN_LIFE_TIME = os.getenv("TOKEN_LIFE_TIME")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=3660)     # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=(60 * 24 * 7))    # 7 days
    ALGORITHM: str = Field(default="HS256")
    DATETIME_FORMAT: str = Field("%Y-%m-%d %H:%M:%S")

    # JWT SETTINGS
    JWT_SECRET_KEY: str = Field('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = Field('JWT_REFRESH_SECRET_KEY')

    # CORE SETTINGS
    TEMPLATES_PATH: str = Field(default="templates")
    STORAGE_PATH = "storage"  # TODO: Add 'STORAGE_PATH' as Field, not str
    SETTLEMENT_HOSTEL_PATH: str = Field(default=(Path(STORAGE_PATH) / "settlement_hostel"))
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_ORIGINS: list[str] = Field(default=["*"])

    # Receive data from '.env' (general 'env' file)
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()
