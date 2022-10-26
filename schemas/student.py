from datetime import datetime
from typing import Dict, Union

from pydantic import BaseModel, validator


class StudentCheckExistanceIn(BaseModel):
    full_name: str
    telephone_number: str


class StudentCheckExistanceOut(BaseModel):
    student: int
    token: str
    expires: datetime


class CreateStudentIn(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    telephone_number: str
    course_id: int
    faculty_id: int
    speciality_id: int
    gender: str

    @validator('first_name')
    def validate_full_name(value):
        first_name = value.split()
        if not first_name:
            raise ValueError("Iм'я студента обов'язкові до заповнення!")
        elif len(first_name) < 2:
            raise ValueError("Iм'я студента обов'язкові до заповнення!")
        return value

    @validator('last_name')
    def validate_full_name(value):
        last_name = value.split()
        if not last_name:
            raise ValueError("Прізвище студента обов'язкові до заповнення!")
        elif len(last_name) < 2:
            raise ValueError("Прізвище студента обов'язкові до заповнення!")
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
    first_name: str
    last_name: str
    middle_name: str
    telephone_number: str
    user_id: int = None
    university_id: int
    faculty_id: int
    speciality_id: int
    course_id: int
    gender: str


class DeleteStudentIn(BaseModel):
    student_id: int
