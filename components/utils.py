from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt
from passlib.context import CryptContext

from settings import ProjectSettings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=ProjectSettings.ACCESS_TOKEN_EXPIRE_SECONDS)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode,  ProjectSettings.JWT_SECRET_KEY, ProjectSettings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=ProjectSettings.REFRESH_TOKEN_EXPIRE_SECONDS)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, ProjectSettings.JWT_REFRESH_SECRET_KEY,  ProjectSettings.ALGORITHM)
    return encoded_jwt
