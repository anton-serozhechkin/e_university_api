from apps.common.exceptions import BackendException
from settings import Settings

from translitua import translit
from random import randint
import hashlib
import os
from datetime import datetime, timedelta
from fastapi import status as http_status


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
    if student[0].user_id:
        raise BackendException(
            message="A student account already exists. Please check your email for details.",
            code=http_status.HTTP_409_CONFLICT
        )
    return student[0].full_name, student[0].faculty_id


def get_token_data(token_data):
    if not token_data:
        raise BackendException(
            message="To register a user, first go to the page for checking the presence of a student in the register.",
            code=http_status.HTTP_404_NOT_FOUND
        )
    if token_data[0].expires < datetime.utcnow():
        raise BackendException(
            message=("Registration time has expired."
                     " Please go to the link to check the availability of students on the register."),
            code=http_status.HTTP_403_FORBIDDEN
        )
    return token_data[0].expires, token_data[0].student_id


def get_token_and_expires():
    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires
