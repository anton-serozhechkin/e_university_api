from datetime import datetime, timedelta
from hashlib import sha1
from os import urandom
from random import randint

from fastapi import status as http_status
from fastapi.security import OAuth2PasswordBearer
from pytz import utc
from sqlalchemy import DATETIME, TypeDecorator
from translitua import translit

from apps.common.exceptions import BackendException
from settings import Settings

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
    if token_data.expires_at < datetime.now(utc):
        raise BackendException(
            message=(
                "Registration time has expired."
                " Please go to the link to check the availability of students on the register."
            ),
            code=http_status.HTTP_403_FORBIDDEN,
        )
    return token_data.expires_at, token_data.student_id


def get_token_and_expires_at():
    token = sha1(urandom(128)).hexdigest()
    expires_at = datetime.now(utc) + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires_at


class AwareDateTime(TypeDecorator):
    """Results returned as aware datetimes, not naive ones.
    """

    impl = DATETIME

    @property
    def python_type(self):
        return type(datetime)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(utc).replace(tzinfo=None)
        return value

    def process_literal_param(self, value, dialect):
        pass

    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=utc)
