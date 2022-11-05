from apps.authorization.models import Role
from apps.common.exceptions import BackendException
from apps.common.services import AsyncCRUDBase


from settings import Settings
from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=Settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, Settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=Settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Settings.JWT_REFRESH_SECRET_KEY, Settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_user(user):
    if not user:
        raise BackendException(message="Login or password is invalid. Please, try again.")


def check_password(user, password):
    if not verify_password(password, user.password):
        raise BackendException(message="Email or password is invalid. Please, try again.")


role_service = AsyncCRUDBase(model=Role)
