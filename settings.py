import pathlib
from pathlib import Path
from functools import lru_cache

import sqlalchemy
from pydantic import BaseSettings, PostgresDsn, Field, validator

__all__ = ['BASE_DIR', 'ProjectSettings', 'TEMPLATES_PATH', 'STORAGE_PATH', 'SETTLEMENT_HOSTEL_PATH']

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATES_PATH = Path(BASE_DIR) / "templates"
STORAGE_PATH = Path(BASE_DIR) / "storage"
SETTLEMENT_HOSTEL_PATH = Path(BASE_DIR) / (Path(STORAGE_PATH) / "settlement_hostel")


class ProjectSettings(BaseSettings):
    # DATABASE SETTINGS
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PASSWORD: str = Field(default='postgres')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DSN: PostgresDsn = Field(default=None)

    # BACK-END SETTINGS
    TOKEN_LIFE_TIME: str = Field(default="TOKEN_LIFE_TIME")
    # 1 hour
    ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(default=3660)
    # 7 days
    REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(default=(60 * 60 * 24 * 7))
    ALGORITHM: str = Field(default="HS256")
    DATETIME_FORMAT: str = Field("%Y-%m-%d %H:%M:%S")

    # JWT SETTINGS
    JWT_SECRET_KEY: str = Field('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = Field('JWT_REFRESH_SECRET_KEY')

    # CORE SETTINGS
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_ORIGINS: list[str] = Field(default=["*"])

    @validator("POSTGRES_DSN", always=True)
    def get_postgres_dsn(cls, value: str, values: dict) -> 'URL' | str:
        if isinstance(value, str):
            return value

        def get_postgres_async_url(values: dict):
            postgres_async_url = sqlalchemy.engine.url.URL(
                scheme="postgres+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=f"{values['POSTGRES_PORT']}",
            )
            return postgres_async_url

        def get_postgres_url(values: dict):
            postgres_url = sqlalchemy.engine.url.URL(
                scheme="postgres",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=f"{values['POSTGRES_PORT']}",
            )
            return postgres_url

        def get_needed_postgres_url(function_name):
            if function_name == 'get_postgres_async_url':
                return get_postgres_async_url(values)
            if function_name == 'get_postgres_url':
                return get_postgres_url(values)

        return get_needed_postgres_url(get_postgres_async_url)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> ProjectSettings:
    return ProjectSettings()


ProjectSettings = get_settings()
