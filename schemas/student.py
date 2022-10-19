from datetime import datetime
from typing import Dict, Union
from components.exceptions import BackendException
from pydantic import BaseModel, validator


class StudentCheckExistanceIn(BaseModel):   # TODO syntax error
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
    def validate_full_name(value):  # TODO may be there is need to use staticmethod decorator
        full_name = value.split()   # TODO use hint or so
        if not full_name:
            raise BackendException(message="Прізвище та ім'я студента обов'язкові до заповнення!")
        elif len(full_name) < 2:
            raise BackendException(message="Прізвище та ім'я студента обов'язкові до заповнення!")
        return value
    
    @validator('telephone_number')
    def validate_telephone_number(value):   # TODO may be there is need to use staticmethod decorator
        if not value:
            raise BackendException(message='Телефонний номер не може бути порожнім!')
        elif len(str(value)) != 12:
            raise BackendException(message='Телефонний номер має містити в собі 12 цифр!')
        return value

    @validator('course_id')
    def validate_course_id(value):  # TODO may be there is need to use staticmethod decorator
        if not value:
            raise BackendException(message='Курс не може бути порожнім!')
        elif value not in range(1, 7):
            raise BackendException(message='Курс моє бути між 1 та 6!')
        return value

    @validator('speciality_id')
    def validate_speciality_id(value):
        if not value:
            raise BackendException(message='Cпеціальність не може бути порожньою!')
        return value

    @validator('faculty_id')
    def validate_faculty_id(value):
        if not value:
            raise BackendException(message='Факультет не може бути порожнім')
        return value

    @validator('gender')
    def validate_gender(value):
        exists_genders = ['Ч', 'М']
        if not value: 
            raise BackendException(message='Стать студента не може бути порожня')
        if value.upper() not in exists_genders:     # TODO use hint or so
            raise BackendException(message='Оберіть стать із запропонованого списку')
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
