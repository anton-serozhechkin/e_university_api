from models.user import user as user_table
from models.student import student as student_table
from models.one_time_token import one_time_token
from models.user_faculty import user_faculty
from db import database
from components.utils import get_hashed_password

import re   
from random import randint
from datetime import datetime

from translitua import translit
from pydantic import BaseModel, validator
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


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
 

class Registration(BaseModel):
    user_id: int
    faculty_id: int
    login: str


@router.post("/registration/", response_model=Registration, tags=["Authorization"])
async def registation(user: RegistrationIn):

    RegistrationIn(
        token=user.token,
        email=user.email,
        password=user.password,
        password_re_check = user.password_re_check)
    
    query = one_time_token.select().where(one_time_token.c.token == user.token)
    token_data = await database.fetch_all(query)

    if not token_data:
        return JSONResponse(status_code=404, content={"message": "Для реєстрації" \
                                            "користувача, спочатку перейдіть на сторінку " \
                                            "перевірки наявності студента в реєстрі"})
 
    for token in token_data: 
        expires = token.expires
        student_id = token.student_id

    datetime_utc_now = datetime.utcnow()

    if datetime_utc_now > expires:
        return JSONResponse(status_code=403, content={"message": "Час на реєстрацію вичерпано. " \
                                            "Будь ласка, перейдіть на посилання для перевірки " \
                                            "наявності студентав реєстрі."})

    query = student_table.select().where(student_table.c.student_id == student_id)
    student = await database.fetch_all(query)
 
    if not student:
        return JSONResponse(status_code=404, content={"message": "Студента не знайдено"})

    for item in student: 
        full_name = item.full_name
        faculty_id = item.faculty_id
        student_user_id = item.user_id

    if student_user_id:
        return JSONResponse(status_code=409, content={"message": "Обліковий запис для студента " \
                                "вже існує. Будь ласка, перевірте деталі на електронній пошті"})

    transliterated_full_name = translit(full_name)
    login = f"{(transliterated_full_name[:4])}-{randint(100,999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = user_table.insert().values(login=login, email=user.email, password=encoded_user_password, role_id=1, is_active=True)
    last_record_id = await database.execute(query)

    query = student_table.update().values(user_id=last_record_id).where(student_table.c.student_id == student_id)
    await database.execute(query)

    query = user_faculty.insert().values(user_id=last_record_id, faculty_id = faculty_id).returning(user_faculty.c.faculty_id)    
    user_faculty_data = await database.execute(query)

    response = {
            "user_id": last_record_id, 
            "faculty_id": user_faculty_data, 
            "login": login
    }

    return response
