from datetime import datetime
from typing import List, Dict, Union
import re

from pydantic import BaseModel, validator


class UsersListViewOut(BaseModel):

    user_id: int
    login: str
    last_vist: datetime = None
    email: str
    is_active: bool = None
    role: List[Dict[str, Union[int, str]]]
    faculties: List[Dict[str, Union[int, str]]]
    university_id: int


class RegistrationOut(BaseModel):
    user_id: int
    faculty_id: int
    login: str


class RegistrationIn(BaseModel):

    token: str
    email: str
    password: str
    password_re_check: str
    
    @validator('email')
    def validate_email(cls, v):
        """
        The method is using for email validation. Only letters (a-z), numbers (0-9) and periods (.) are allowed
        :return: True or not None string
        """
        specials = '!#$%&\'*+-/=?^_`{|?.'
        specials = re.escape(specials)
        regex = re.compile('^(?![' + specials + '])'
                           '(?!.*[' + specials + ']{2})'
                           '(?!.*[' + specials + ']$)'
                           '[A-Za-z0-9' + specials + ']+(?<!['+ specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
        message = False

        if not v:
            message = "Електронний адрес не може бути порожнім"

        elif not re.fullmatch(regex, v):
            message = f"Невірний формат адресу електронної пошти: {v}."

        if message:
            raise ValueError(message)

        return v

    @validator('password_re_check')
    def validate_password(cls, v, values):
        password = values.get('password')

        if not password or not v:
            raise ValueError('Паролі не можуть бути порожніми')

        if password != v:
            raise ValueError('Введені паролі не співпадають')

        return v


class AuthOut(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


class CreateUserIn(BaseModel):
    
    email: str
    password: str
    password_re_check: str
    role_id: int
    faculty_id: List[int]

    @validator('email')
    def validate_email(cls, v):
        """
        The method is using for email validation. Only letters (a-z), numbers (0-9) and periods (.) are allowed
        :return: True or not None string
        """
        specials = '!#$%&\'*+-/=?^_`{|?.'
        specials = re.escape(specials)
        regex = re.compile('^(?![' + specials + '])'
                           '(?!.*[' + specials + ']{2})'
                           '(?!.*[' + specials + ']$)'
                           '[A-Za-z0-9' + specials + ']+(?<!['+ specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
        message = False
        if not v:
            message = "Електронний адрес не може бути порожнім"
        elif not re.fullmatch(regex, v):
            message = f"Невірний формат адреси електронної пошти: {v}."
        if message:
            raise ValueError(message)
        
        return v

    @validator('password_re_check')
    def validate_password(cls, v, values):
        password = values.get('password')

        if not password or not v:
            raise ValueError('Паролі не можуть бути порожніми')

        if password != v:
            raise ValueError('Введені паролі не співпадають')

        return v


class CreateUserOut(BaseModel):
    user_id: int


class TokenPayload(BaseModel):
    exp: int
    sub: str


class UserOut(BaseModel):
    user_id: int
    login: str
    last_visit: datetime = None
    email: str
    is_active: bool = None
    role: List[Dict[str, Union[int, str]]]
    faculties: List[Dict[str, Union[int, str]]]
    university_id: int


class UserIn(TokenPayload):
    user_id: int
