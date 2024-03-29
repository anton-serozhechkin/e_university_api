from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pytz import utc

from apps.authorization.models import Role
from apps.common.exceptions import BackendException
from apps.common.services import AsyncCRUDBase, ModelType
from settings import Settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(utc) + expires_delta
    else:
        expires_delta = datetime.now(utc) + timedelta(
            seconds=Settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, Settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(utc) + expires_delta
    else:
        expires_delta = datetime.now(utc) + timedelta(
            seconds=Settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, Settings.JWT_REFRESH_SECRET_KEY, Settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_user(user: Optional[ModelType]) -> None:
    if not user:
        raise BackendException(
            message="Login or password is invalid. Please, try again."
        )


def verify_password(user: ModelType, password: str) -> None:
    if not check_password(password, user.password):
        raise BackendException(
            message="Login or password is invalid. Please, try again."
        )


def check_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


role_service = AsyncCRUDBase(model=Role)
