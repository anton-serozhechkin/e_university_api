from users.schemas import *
from users.models import user_list_view
from users.models import students_list_view
from users.models import user as user_table
from users.models import student as student_table
from users.models import user_faculty
from users.models import one_time_token
from settings.globals import TOKEN_LIFE_TIME
from components.utils import get_hashed_password
from db import database

from random import randint
from typing import List, Union
from datetime import datetime, timedelta
from jose import jwt

import hashlib
import os

from translitua import translit
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import ValidationError


users_router = APIRouter()


from settings.globals import (
    ALGORITHM,
    JWT_SECRET_KEY
)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login/",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Термін дії токена закінчився",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не вдалося перевірити облікові дані",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    query = user_table.select().where(user_table.c.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача не знайдено",
        )

    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    user = await database.fetch_one(query)

    return user


@users_router.post("/check-student-existence/", response_model=StudentCheckExistenceOut, tags=["Authorization"])
async def check_student(student: StudentCheckExistenceIn):

    query = student_table.select().where(student_table.c.full_name == student.full_name, 
                                    student_table.c.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Дані про студента не знайдено. " \
                                                                "Будь ласка, спробуйте ще раз."})

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=TOKEN_LIFE_TIME)

    query = one_time_token.insert().values(student_id=student_id, token=token,
                                           expires=expires).returning(one_time_token.c.token_id)                      
    last_record_id = await database.execute(query)

    query = one_time_token.select().where(one_time_token.c.token_id == last_record_id)
    result = await database.fetch_one(query)

    response = {
                'token': result.token,
                'student': result.student_id, 
                'expires': result.expires
    }

    return response


@users_router.get("/{university_id}/users/", response_model=List[UsersListViewOut], tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user = Depends(get_current_user)):
    query = user_list_view.select().where(user_list_view.c.university_id == university_id)
    response = await database.fetch_all(query)
    return response


@users_router.post("/{university_id}/users/", response_model=CreateUserOut, tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth = Depends(get_current_user)):
    
    CreateUserIn(
        email=user.email,
        password=user.password,
        password_re_check = user.password_re_check,
        role_id =  user.role_id,
        faculty_id = user.faculty_id
    )

    hashed_password = get_hashed_password(user.password)

    login = f"{(user.email[:4])}-{randint(100,999)}".lower()

    query = user_table.insert().values(login=login, password=hashed_password, 
                                        email=user.email, role_id=user.role_id, 
                                        is_active=False)

    last_record_id = await database.execute(query)

    for faculty_id in user.faculty_id:
        query = user_faculty.insert().values(user_id=last_record_id, 
                                            faculty_id = faculty_id)
        await database.execute(query)

    return {
       "user_id": last_record_id
    }


@users_router.delete("/{university_id}/users/", tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth = Depends(get_current_user)):
    query = user_table.delete().where(user_table.c.user_id == delete_user.user_id)
    
    await database.execute(query)

    return {
        "user_id": delete_user.user_id
    }

@users_router.post("/registration/", response_model=RegistrationOut, tags=["Authorization"])
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


@users_router.post("/{university_id}/students/", response_model=CreateStudentOut, tags=["Admin dashboard"])
async def create_student(university_id: int, student: CreateStudentIn, auth = Depends(get_current_user)):
    
    CreateStudentIn(
        full_name=student.full_name,
        telephone_number=student.telephone_number,
        course_id=student.course_id,
        faculty_id=student.faculty_id,
        speciality_id=student.speciality_id,
        gender=student.gender)

    query = student_table.insert().values(full_name=student.full_name, telephone_number=student.telephone_number,
                                        course_id=student.course_id, faculty_id=student.faculty_id,
                                        speciality_id=student.speciality_id, gender=student.gender.upper())

    student_id = await database.execute(query)

    return {
       "student_id": student_id
    }


@users_router.get("/{university_id}/students/", response_model=List[StudentsListOut], tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None , user = Depends(get_current_user)):
    if faculty_id: 
        query = students_list_view.select().where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = students_list_view.select().where(students_list_view.c.university_id == university_id)
        
    return await database.fetch_all(query)


@users_router.delete("/{university_id}/students/", tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth = Depends(get_current_user)):
    query = student_table.delete().where(student_table.c.student_id == delete_student.student_id)
    
    await database.execute(query)

    return {
        "student_id": delete_student.student_id
    }


@users_router.get('/me/', summary='Get information about current user', response_model=UserOut, tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return user
