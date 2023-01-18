import logging
from functools import lru_cache
from pathlib import Path
from typing import List, Union

from pydantic import BaseSettings, Extra, Field, PostgresDsn, validator
from sqlalchemy.engine.url import URL

__all__ = [
    "BASE_DIR",
    "Settings",
    "TEMPLATES_PATH",
    "STORAGE_PATH",
    "SETTLEMENT_HOSTEL_PATH",
    "SERVICES_PATH",
    "HOSTEL_BOOKING_TEMPLATE",
    "HOSTEL_WARRANT_TEMPLATE",
    "WARRANT_HOSTEL_ACCOMMODATION_PATH",
]

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_PATH = BASE_DIR / "apps" / "templates"
STORAGE_PATH = BASE_DIR / "apps" / "storage"
SERVICES_PATH = BASE_DIR / "apps" / "services"
SETTLEMENT_HOSTEL_PATH = STORAGE_PATH / "services" / "settlement_hostel"
WARRANT_HOSTEL_ACCOMMODATION_PATH = SETTLEMENT_HOSTEL_PATH / "warrants"

HOSTEL_BOOKING_TEMPLATE = "hostel_booking_template.docx"
HOSTEL_WARRANT_TEMPLATE = "hostel_warrant_template.docx"


def _build_db_dsn(values: dict, async_dsn: bool = False) -> URL:
    driver_name = "postgresql"
    if async_dsn:
        driver_name += "+asyncpg"
    # TODO: Uncomment when "databases" dependency will be removed.
    # return URL.create(
    #     drivername=driver_name,
    #     username=values["POSTGRES_USER"],
    #     password=values["POSTGRES_PASSWORD"],
    #     host=values["POSTGRES_HOST"],
    #     port=values["POSTGRES_PORT"],
    #     database=values["POSTGRES_DB"]
    # )
    # TODO: Remove when "databases" dependency will be removed.
    username = values["POSTGRES_USER"]
    password = values["POSTGRES_PASSWORD"]
    host = values["POSTGRES_HOST"]
    port = values["POSTGRES_PORT"]
    database = values["POSTGRES_DB"]
    return f"{driver_name}://{username}:{password}@{host}:{port}/{database}"


class MainSettings(BaseSettings):
    # DATABASE SETTINGS
    POSTGRES_ECHO: bool = Field(default=False)
    POSTGRES_DB: str = Field(default="postgres")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="0.0.0.0")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DSN: PostgresDsn = Field(default=None)
    POSTGRES_DSN_ASYNC: PostgresDsn = Field(default=None)

    # BACK-END SETTINGS
    DEBUG: bool = Field(default=False)
    ENABLE_OPENAPI: bool = Field(default=False)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    WORKERS_COUNT: int = Field(default=1)
    TRUSTED_HOSTS: List[str] = Field(default=["*"])
    DATETIME_FORMAT: str = Field("%Y-%m-%d %H:%M:%S")

    # ONE-TIME TOKEN SETTINGS
    TOKEN_LIFE_TIME: int = Field(default=3600)

    # JWT SETTINGS
    JWT_SECRET_KEY: str = Field("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = Field("JWT_REFRESH_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(default=3660)  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(default=(60 * 60 * 24 * 7))  # 7 days
    JWT_ALGORITHM: str = Field(default="HS256")

    # CORS SETTINGS
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_ORIGINS: List[str] = Field(default=["*"])

    # LOGGING SETTINGS
    LOG_LEVEL: int = Field(default=logging.WARNING)
    LOG_USE_COLORS: bool = Field(default=False)

    # SEND MAIL SETTINGS
    MAIL_USERNAME: str = Field(default="8f2d4fcedddbb9")
    MAIL_PASSWORD: str = Field(default="6bab9ee9d83cf2")
    MAIL_FROM: str = Field(default="noreply@gmail.com")
    MAIL_PORT: int = Field(default=2525)
    MAIL_SERVER: str = Field(default="smtp.mailtrap.io")
    MAIL_FROM_NAME: str = Field(default="admin")
    MAIL_TLS: bool = Field(default=True)
    MAIL_SSL: bool = Field(default=False)
    USE_CREDENTIALS: bool = Field(default=True)
    TEMPLATE_FOLDER: str = Field(default="./apps/templates/email")

    class Config(BaseSettings.Config):
        extra = Extra.ignore
        env_file = ".env"
        env_file_encoding = "UTF-8"
        env_nested_delimiter = "__"

    @validator("POSTGRES_DSN", always=True)
    def validate_database_url(
        cls, value: Union[str, int], values: dict
    ) -> Union[URL, str]:
        if value is None:
            return _build_db_dsn(values=values)
        return value

    @validator("POSTGRES_DSN_ASYNC", always=True)
    def validate_database_url_async(
        cls, value: Union[str, int], values: dict
    ) -> Union[URL, str]:
        if value is None:
            return _build_db_dsn(values=values, async_dsn=True)
        return value


@lru_cache()
def get_settings() -> MainSettings:
    return MainSettings()


Settings: MainSettings = get_settings()

if Settings.DEBUG:
    import pprint  # noqa

    pprint.pprint(Settings.dict())
