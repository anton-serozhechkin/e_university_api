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


class DeleteUserIn(BaseModel):
    user_id: int


class StudentCheckExistanceIn(BaseModel):
    full_name: str
    telephone_number: str


class StudentCheckExistanceOut(BaseModel):
    student: int
    token: str
    expires: datetime

class CreateStudentIn(BaseModel):
    full_name: str
    telephone_number: str
    course_id: int
    faculty_id: int
    speciality_id: int
    gender: str

    @validator('full_name')
    def validate_full_name(value):
        full_name = value.split()
        if not full_name:
            raise ValueError("Прізвище та ім'я студента обов'язкові до заповнення!")
        elif len(full_name) < 2:
            raise ValueError("Прізвище та ім'я студента обов'язкові до заповнення!")
        return value
    
    @validator('telephone_number')
    def validate_telephone_number(value):
        if not value:
            raise ValueError('Телефонний номер не може бути порожнім!')
        elif len(str(value)) != 12:
            raise ValueError('Телефонний номер має містити в собі 12 цифр!')
        return value

    @validator('course_id')
    def validate_course_id(value):
        if not value:
            raise ValueError('Курс не може бути порожнім!')
        elif value not in range(1, 7):
            raise ValueError('Курс моє бути між 1 та 6!')
        return value

    @validator('speciality_id')
    def validate_speciality_id(value):
        if not value:
            raise ValueError('Cпеціальність не може бути порожньою!')
        return value

    @validator('faculty_id')
    def validate_faculty_id(value):
        if not value:
            raise ValueError('Факультет не може бути порожнім')
        return value

    @validator('gender')
    def validate_gender(value):
        exists_genders = ['Ч', 'М']
        if not value: 
            raise ValueError('Стать студента не може бути порожня')
        if value.upper() not in exists_genders:
            raise ValueError('Оберіть стать із запропонованого списку')
        return value


class CreateStudentOut(BaseModel):
    student_id: int       


class StudentsListOut(BaseModel):
    student_id: int       
    student_full_name: str
    telephone_number: str
    user_id: int = None
    university_id: int
    faculty_id: int
    speciality_id: int
    course_id: int
    gender: str


class DeleteStudentIn(BaseModel):
    student_id: int
