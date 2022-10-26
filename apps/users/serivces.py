from settings import Settings

from translitua import translit
from random import randint
import hashlib
import os
from datetime import datetime, timedelta


def get_login(data):
    return f"{(data[:4])}-{randint(100, 999)}".lower()


def get_login_full_name(full_name):
    transliterated_full_name = translit(full_name)
    return get_login(transliterated_full_name)


def get_student_attr(student):
    full_name, faculty_id, student_user_id = '', 0, 0
    for item in student:
        full_name = item.full_name
        faculty_id = item.faculty_id
        student_user_id = item.user_id
    return full_name, faculty_id, student_user_id


def get_token_data(token_data):
    expires, student_id = None, 0
    for token in token_data:
        expires = token.expires
        student_id = token.student_id
    return expires, student_id


def get_token_and_expires():
    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires
