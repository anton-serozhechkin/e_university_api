from apps.components.utils import get_hashed_password
from apps.core.db import database
from apps.users.models import User, user_list_view, Student, OneTimeToken, UserFaculty, students_list_view
from apps.users.schemas import UserOut, TokenPayload, UsersListViewOut, CreateUserOut, CreateUserIn, DeleteUserIn, \
    RegistrationOut, RegistrationIn, CreateStudentOut, CreateStudentIn, StudentsListOut, DeleteStudentIn, UserIn, \
    StudentCheckExistenceIn, StudentCheckExistenceOut
from settings import Settings

from random import randint
from typing import List, Union
from datetime import datetime, timedelta
from jose import jwt

import hashlib
import os

from sqlalchemy import select, insert, delete, update
from translitua import translit
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import ValidationError


router = APIRouter()

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login/",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Термін дії токена закінчився",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не вдалося перевірити облікові дані",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = select(User).where(User.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача не знайдено",
        )

    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    user = await database.fetch_one(query)

    return user


@router.post("/check-student-existance", response_model=StudentCheckExistenceOut, tags=["Authorization"])
async def check_student(student: StudentCheckExistenceIn):

    query = select(Student).where(Student.full_name == student.full_name,
                                  Student.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Дані про студента не знайдено. " \
                                                                 "Будь ласка, спробуйте ще раз."})

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)

    query = insert(OneTimeToken).values(student_id=student_id, token=token,
                                        expires=expires).returning(OneTimeToken.token_id)
    last_record_id = await database.execute(query)

    query = select(OneTimeToken).where(OneTimeToken.token_id == last_record_id)
    result = await database.fetch_one(query)

    response = {
                'token': result.token,
                'student': result.student_id, 
                'expires': result.expires
    }

    return response


@router.get("/{university_id}/users/", response_model=List[UsersListViewOut], tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_list_view).where(user_list_view.c.university_id == university_id)
    response = await database.fetch_all(query)
    return response


@router.post("/{university_id}/users/", response_model=CreateUserOut, tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth=Depends(get_current_user)):
    CreateUserIn(
        email=user.email,
        password=user.password,
        password_re_check=user.password_re_check,
        role_id=user.role_id,
        faculty_id=user.faculty_id
    )

    hashed_password = get_hashed_password(user.password)

    login = f"{(user.email[:4])}-{randint(100, 999)}".lower()

    query = insert(User).values(login=login, password=hashed_password,
                                email=user.email, role_id=user.role_id,
                                is_active=False)

    last_record_id = await database.execute(query)

    for faculty_id in user.faculty_id:
        query = insert(UserFaculty).values(user_id=last_record_id,
                                           faculty_id=faculty_id)
        await database.execute(query)

    return {
        "user_id": last_record_id
    }


@router.delete("/{university_id}/users/", tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth=Depends(get_current_user)):
    query = delete(User).where(User.user_id == delete_user.user_id)

    await database.execute(query)

    return {
        "user_id": delete_user.user_id
    }


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


@router.post("/{university_id}/students/", response_model=CreateStudentOut, tags=["Admin dashboard"])
async def create_student(university_id: int, student: CreateStudentIn, auth=Depends(get_current_user)):
    CreateStudentIn(
        full_name=student.full_name,
        telephone_number=student.telephone_number,
        course_id=student.course_id,
        faculty_id=student.faculty_id,
        speciality_id=student.speciality_id,
        gender=student.gender)

    query = insert(Student).values(full_name=student.full_name, telephone_number=student.telephone_number,
                                   course_id=student.course_id, faculty_id=student.faculty_id,
                                   speciality_id=student.speciality_id, gender=student.gender.upper())

    student_id = await database.execute(query)

    return {
        "student_id": student_id
    }


@router.get("/{university_id}/students/", response_model=List[StudentsListOut], tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(get_current_user)):
    if faculty_id:
        query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = select(students_list_view).where(students_list_view.c.university_id == university_id)

    return await database.fetch_all(query)


@router.delete("/{university_id}/students/", tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    query = delete(Student).where(Student.student_id == delete_student.student_id)

    await database.execute(query)

    return {
        "student_id": delete_student.student_id
    }


@router.get('/me', summary='Отримати інформацію про поточного користувача, який увійшов у систему', response_model=UserOut,
            tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return user
