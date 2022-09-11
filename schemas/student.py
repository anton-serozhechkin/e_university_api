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
    full_name: Dict[str, str]
    telephone_number: str
    course_id: int
    faculty_id: int
    speciality_id: int
    gender: str

@validator('full_name')
def validate_full_name(value):
    full_name = value.split()
    if not full_name:
        
        raise ValueError("Прізвище та ім'я студента обовязкові до заповнення!")
    elif len(full_name) < 2:
        raise ValueError("Прізвище та ім'я студента обовязкові до заповнення!")
    
    return value
    
@validator('telephone_number')
def validate_telephone_number(value, number_len=9):
    if not value:
        raise ValueError('Телефонний номер не може бути порожнім')

    elif len(str(value)) != number_len or len(str(value)) <= 1:
        raise ValueError('Телефонний номер має містити в собі 9 символів без коду країни')

    return value

@validator('course_id')
def validate_course_id(value):
    if not value:
        raise ValueError('Курс не може бути порожнім')
    elif value < 1 or value > 6:
        raise ValueError('Курс моє бути між 1 та 6!')
    
    return value

@validator('speciality_id')
def validate_speciality_id(value):
    if not value:
        raise ValueError('Cпеціальність не може бути порожня')

    elif value < 1 or value > 25:
        raise ValueError('Має бути обрана 1 із 25 спеціальностей Університету')
    
    return value

@validator('faculty_id')
def validate_faculty_id(value):
    if not value:
        raise ValueError('Факультет не може бути порожнім')
    
    elif value < 1 or value > 6:
        raise ValueError('Має бути обран 1 із 6 діючих факультетів Університету')

    return value

@validator('gender')
def validate_gender(value):
    exists_genders = ['Ч', 'М']
    if not value: 
        raise ValueError('Стать студента не може бути порожня')

    if value not in exists_genders:
        raise ValueError('Оберіть стать із запропонованого списку')
    
    return value


class CreateStudentOut(BaseModel):
    user_id: int


    
       


    




