from apps.common.exceptions import BackendException
from settings import Settings

from translitua import translit
from random import randint
import hashlib
import os
from datetime import datetime, timedelta
from fastapi import status as http_status
from fastapi.security import OAuth2PasswordBearer


reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_generated_username(last_name: str, first_name: str) -> str:
    if len(last_name) < 4:
        last_name = last_name.join(first_name)
    transliterated_last_name = translit(last_name)
    return add_random_digits_and_cut_username(transliterated_last_name)


def add_random_digits_and_cut_username(data: str) -> str:
    return f"{(data[:4])}-{randint(100, 999)}".lower()


def get_student_attr(student):
    if not student:
        raise BackendException(
            message="Student is not found.", code=http_status.HTTP_404_NOT_FOUND
        )
    if student.user_id:
        raise BackendException(
            message="A user account already exists. Please check your email for details.",
            code=http_status.HTTP_409_CONFLICT,
        )
    return student.first_name, student.last_name, student.faculty_id


def get_token_data(token_data):
    if not token_data:
        raise BackendException(
            message="To register a user, first go to the page for checking the presence of a student in the register.",
            code=http_status.HTTP_404_NOT_FOUND,
        )
    if token_data.expires < datetime.utcnow():
        raise BackendException(
            message=(
                "Registration time has expired."
                " Please go to the link to check the availability of students on the register."
            ),
            code=http_status.HTTP_403_FORBIDDEN,
        )
    return token_data.expires, token_data.student_id


def get_token_and_expires():
    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires
