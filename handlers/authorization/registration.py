from sqlalchemy import update, select, insert

from models.user import User
from models.student import Student
from models.one_time_token import OneTimeToken
from models.user_faculty import UserFaculty
from db import database
from components.utils import get_hashed_password
from schemas.user import RegistrationIn, RegistrationOut

from random import randint
from datetime import datetime

from translitua import translit
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/registration", response_model=RegistrationOut, tags=["Authorization"])
async def registation(user: RegistrationIn):
    RegistrationIn(
        token=user.token,
        email=user.email,
        password=user.password,
        password_re_check=user.password_re_check)

    query = select(OneTimeToken).where(OneTimeToken.token == user.token)
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

    query = select(Student).where(Student.student_id == student_id)
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
    login = f"{(transliterated_full_name[:4])}-{randint(100, 999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = insert(User).values(login=login, email=user.email, password=encoded_user_password, role_id=1,
                                is_active=True)
    last_record_id = await database.execute(query)

    query = update(Student).values(user_id=last_record_id).where(Student.student_id == student_id)
    await database.execute(query)

    query = insert(UserFaculty).values(user_id=last_record_id, faculty_id=faculty_id).returning(
        UserFaculty.faculty_id)
    user_faculty_data = await database.execute(query)

    response = {
        "user_id": last_record_id,
        "faculty_id": user_faculty_data,
        "login": login
    }

    return response
