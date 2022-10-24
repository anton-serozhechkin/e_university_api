from apps.common.exceptions import BackendException
from apps.common.utils import get_hashed_password
from apps.common.db import database
from apps.users.models import User, user_list_view, Student, OneTimeToken, UserFaculty, students_list_view
from apps.users.schemas import UserOut, TokenPayload, UsersListViewOut, CreateUserOut, CreateUserIn, DeleteUserIn, \
    RegistrationOut, RegistrationIn, CreateStudentOut, CreateStudentIn, StudentsListOut, UserIn, DeleteStudentIn, \
    StudentCheckExistanceOut, StudentCheckExistanceIn
from settings import Settings

from random import randint
from typing import List, Union
from datetime import datetime, timedelta
from jose import jwt

import hashlib
import os

from sqlalchemy import select, insert, delete, update
from translitua import translit
from fastapi import Depends, APIRouter, HTTPException, status as http_status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from apps.jsend import JSENDOutSchema

users_router = APIRouter()

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)       # TODO spelling mistake 'reusable'


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Token data has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Credential verification failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

    query = select(User).where(User.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise BackendException(
            message="User not found",
            code=http_status.HTTP_404_NOT_FOUND
        )

    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    user = await database.fetch_one(query)

    return user


@users_router.post("/check-student-existance", response_model=JSENDOutSchema[StudentCheckExistanceOut],
                   tags=["Authorization"])  # TODO spelling mistake, there is need to check path in other modules
async def check_student(student: StudentCheckExistanceIn):

    query = select(Student).where(Student.full_name == student.full_name,
                                  Student.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        raise BackendException(
            message="Student data was not found. Please, try again.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)

    query = insert(OneTimeToken).values(student_id=student_id, token=token,
                                        expires=expires).returning(OneTimeToken.token_id)
    last_record_id = await database.execute(query)

    query = select(OneTimeToken).where(OneTimeToken.token_id == last_record_id)
    result = await database.fetch_one(query)

    return {
        "data": {
            'token': result.token,
            'student': result.student_id,
            'expires': result.expires
        },
        "message": f"Get information of student with id {result.student_id}"
    }


@users_router.get("/{university_id}/users/", response_model=JSENDOutSchema[List[UsersListViewOut]],
                  tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_list_view).where(user_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got user list of the university with id {university_id}"
    }


@users_router.post("/{university_id}/users/", response_model=JSENDOutSchema[CreateUserOut], tags=["SuperAdmin dashboard"])
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
        "data": {
            "user_id": last_record_id
        },
        "message": f"Created user with id {last_record_id}"
    }


@users_router.delete("/{university_id}/users/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth=Depends(get_current_user)):
    query = delete(User).where(User.user_id == delete_user.user_id)

    await database.execute(query)

    return {
        "data": {
            "user_id": delete_user.user_id
        },
        "message": f"Deleted user with id {delete_user.user_id}"
    }


@users_router.post("/registration", response_model=JSENDOutSchema[RegistrationOut], tags=["Authorization"])
async def registration(user: RegistrationIn):

    RegistrationIn(
        token=user.token,
        email=user.email,
        password=user.password,
        password_re_check=user.password_re_check)

    query = select(OneTimeToken).where(OneTimeToken.token == user.token)
    token_data = await database.fetch_all(query)

    if not token_data:
        raise BackendException(
            message="To register a user, first go to the page for checking the presence of a student in the register.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    for token in token_data:
        expires = token.expires
        student_id = token.student_id

    datetime_utc_now = datetime.utcnow()

    if datetime_utc_now > expires:  # TODO Local variable 'expires' might be referenced before assignment
        raise BackendException(
            message=("Registration time has expired."
                     " Please go to the link to check the availability of students on the register."),
            code=http_status.HTTP_403_FORBIDDEN
        )

    query = select(Student).where(Student.student_id == student_id)
    student = await database.fetch_all(query)

    if not student:
        raise BackendException(
            message="Student is not found.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    for item in student:
        full_name = item.full_name
        faculty_id = item.faculty_id
        student_user_id = item.user_id

    if student_user_id:  # TODO Local variable 'student_user_id' might be referenced before assignment
        raise BackendException(
            message="A student account already exists. Please check your email for details.",
            code=http_status.HTTP_409_CONFLICT
        )

    transliterated_full_name = translit(full_name)  # TODO Local variable 'full_name' might be referenced before assignment
    login = f"{(transliterated_full_name[:4])}-{randint(100, 999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = insert(User).values(login=login, email=user.email, password=encoded_user_password, role_id=1,
                                is_active=True)
    last_record_id = await database.execute(query)

    query = update(Student).values(user_id=last_record_id).where(Student.student_id == student_id)
    await database.execute(query)

    query = insert(UserFaculty).values(user_id=last_record_id, faculty_id=faculty_id).returning(
        UserFaculty.faculty_id)     # TODO Local variable 'faculty_id' might be referenced before assignment
    user_faculty_data = await database.execute(query)

    return {
        "data": {
            "user_id": last_record_id,
            "faculty_id": user_faculty_data,
            "login": login
        },
        "message": f"User with id {last_record_id} was registered successfully"
    }


@users_router.post("/{university_id}/students/", response_model=JSENDOutSchema[CreateStudentOut], tags=["Admin dashboard"])
#TODO after input id of the non-existent university it creates student
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
        "data": {
            "student_id": student_id
        },
        "message": f"Created student {student.full_name}"
    }


@users_router.get("/{university_id}/students/", response_model=JSENDOutSchema[List[StudentsListOut]],
                  tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(get_current_user)):  #TODO after input id of the non-existent university it returns the students
    if faculty_id:
        query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = select(students_list_view).where(students_list_view.c.university_id == university_id)

    return {
        "data": await database.fetch_all(query),
        "message": f"Got students list of the university with id {university_id}"
    }


@users_router.delete("/{university_id}/students/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    query = delete(Student).where(Student.student_id == delete_student.student_id)

    await database.execute(query)
    # TODO: in response key data has empty dict value, not like it's discribed
    return {
        "data": {
            "student_id": delete_student.student_id
        },
        "message": f"Deleted student with id {delete_student.student_id}"
    }


@users_router.get('/me', summary='Отримати інформацію про поточного користувача, який увійшов у систему',
                  response_model=JSENDOutSchema[UserOut], tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return {
        "data": user,
        "message": "Got user information"
    }
