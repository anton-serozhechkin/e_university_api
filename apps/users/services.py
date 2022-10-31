from apps.common.db import database
from apps.common.exceptions import BackendException
from apps.common.services import AsyncCRUDBase
from apps.users.models import OneTimeToken, Student, User, user_list_view, students_list_view
from apps.users.schemas import TokenPayload, UserOut
from settings import Settings

from translitua import translit
from random import randint
import hashlib
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status as http_status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select, insert, delete, update


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Token data has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Credential verification failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

    query = select(User).where(User.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise BackendException(
            message="User not found",
            code=http_status.HTTP_404_NOT_FOUND
        )
    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    return await database.fetch_one(query)


def get_login(data):
    return f"{(data[:4])}-{randint(100, 999)}".lower()


def get_login_full_name(full_name):
    transliterated_full_name = translit(full_name)
    return get_login(transliterated_full_name)


def get_student_attr(student):
    if not student:
        raise BackendException(
            message="Student is not found.",
            code=http_status.HTTP_404_NOT_FOUND
        )
    if student.user_id:
        raise BackendException(
            message="A student account already exists. Please check your email for details.",
            code=http_status.HTTP_409_CONFLICT
        )
    return student.full_name, student.faculty_id


def get_token_data(token_data):
    if not token_data:
        raise BackendException(
            message="To register a user, first go to the page for checking the presence of a student in the register.",
            code=http_status.HTTP_404_NOT_FOUND
        )
    if token_data.expires < datetime.utcnow():
        raise BackendException(
            message=("Registration time has expired."
                     " Please go to the link to check the availability of students on the register."),
            code=http_status.HTTP_403_FORBIDDEN
        )
    return token_data.expires, token_data.student_id


def get_token_and_expires():
    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires


student_service = AsyncCRUDBase(model=Student)
one_time_token_service = AsyncCRUDBase(model=OneTimeToken)
user_list_service = AsyncCRUDBase(model=user_list_view)
user_service = AsyncCRUDBase(model=User)
student_list_service = AsyncCRUDBase(model=students_list_view)
