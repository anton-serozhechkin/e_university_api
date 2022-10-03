import logging
from pathlib import Path
from functools import lru_cache

from sqlalchemy.engine.url import URL
from pydantic import BaseSettings, PostgresDsn, Field, validator

__all__ = ['BASE_DIR', 'Settings', 'TEMPLATES_PATH', 'STORAGE_PATH', 'SETTLEMENT_HOSTEL_PATH']

BASE_DIR = pathlib.Path(__file__).resolve().parent

TEMPLATES_PATH = BASE_DIR / "templates"
STORAGE_PATH = BASE_DIR / "storage"
SETTLEMENT_HOSTEL_PATH = BASE_DIR / (Path(STORAGE_PATH) / "settlement_hostel")


def _build_db_dsn(values: dict, async_dsn: bool = False) -> 'URL':
    driver_name = "postgresql"
    if async_dsn:
        driver_name += "+asyncpg"
    return URL.create(
        drivername=driver_name,
        user=values["POSTGRES_USER"],
        password=values["POSTGRES_PASSWORD"],
        host=values["POSTGRES_HOST"],
        port=f"{values['POSTGRES_PORT']}",
        database=values["POSTGRES_DB"]
    )


class MainSettings(BaseSettings):
    # DATABASE SETTINGS
    POSTGRES_ECHO: bool = Field(default=False)
    POSTGRES_DB: str = Field(default="postgres")
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_HOST: str = Field(default='0.0.0.0')
    POSTGRES_PASSWORD: str = Field(default='postgres')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DSN: PostgresDsn = Field(default=None)
    POSTGRES_DSN_ASYNC: PostgresDsn = Field(default=None)

    # BACK-END SETTINGS
    DEBUG: bool = Field(default=False)
    ENABLE_OPENAPI: bool = Field(default=False)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    WORKERS_COUNT: int = Field(default=1)
    TRUSTED_HOSTS: list[str] = Field(default=["*"])
    DATETIME_FORMAT: str = Field("%Y-%m-%d %H:%M:%S")

    # JWT SETTINGS
    JWT_SECRET_KEY: str = Field('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = Field('JWT_REFRESH_SECRET_KEY')
    JWT_TOKEN_LIFE_TIME: str = Field(default="TOKEN_LIFE_TIME")
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(default=3660)  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(default=(60 * 60 * 24 * 7))  # 7 days
    JWT_ALGORITHM: str = Field(default="HS256")

    # CORE SETTINGS
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_ORIGINS: list[str] = Field(default=["*"])

    # LOGGING SETTINGS
    LOG_LEVEL: int = Field(default=logging.WARNING)
    LOG_USE_COLORS: bool = Field(default=False)

    @validator("POSTGRES_URL", always=True)
    def validate_database_url(cls, value: str, values: dict) -> 'URL' | str:
        """Construct PostgreSQL DSN"""
        if value is None:
            return _build_db_dsn(values=values)
        return value

    @validator("POSTGRES_URL_ASYNC", always=True)
    def validate_database_url_async(cls, value: str, values: dict) -> 'URL' | str:
        """Construct async (with asyncpg driver) PostgreSQL DSN"""
        if value is None:
            return _build_db_dsn(values=values, async_dsn=True)
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> MainSettings:
    return Settings()


Settings: MainSettings = get_settings()

if Settings.DEBUG:
    import pprint  # noqa

    pprint.pprint(Settings.dict())
