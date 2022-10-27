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
    return student[0].full_name, student[0].faculty_id, student[0].user_id


def get_token_data(token_data):
    return token_data[0].expires, token_data[0].student_id


def get_token_and_expires():
    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)
    return token, expires
