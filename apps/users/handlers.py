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
from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema


users_router = APIRouter()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)  # TODO spelling mistake 'reusable'


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


@users_router.post("/check-student-existance",
                   name="create_student_existence",
                   response_model=JSENDOutSchema[StudentCheckExistanceOut],
                   summary="Check user existence",
                   responses={
                       200: {"description": "Successful check user existence response"},
                       404: {"model": JSENDFailOutSchema, "description": "Invalid input data response"},
                       422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                   },
                   tags=["Authorization"])  # TODO spelling mistake, there is need to check path in other modules
async def check_student(student: StudentCheckExistanceIn):
    """
        **Check student existence in the database**

        **Input**:
        - **full name**: full name of the student in the database
        - **telephone number**: telephone number, must be 12 digits

        **Return**: student id; token, which is used for registering user; token expires datetime
    """
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


@users_router.get("/{university_id}/users/",
                  name="read_users_list",
                  response_model=JSENDOutSchema[List[UsersListViewOut]],
                  summary="Get university users list",
                  responses={
                      200: {"description": "Successful get all users list of the university response"},
                      422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                  },
                  tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_list_view).where(user_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got user list of the university with id {university_id}"
    }


@users_router.post("/{university_id}/users/",
                   name="create_user",
                   response_model=JSENDOutSchema[CreateUserOut],
                   summary="Create university user",
                   responses={
                       200: {"description": "Successful create university user response"},
                       422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                   },
                   tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth=Depends(get_current_user)):
    """
        **Create university user**

        **Path**:
        - **university_id**: university id for creating user

        **Input**:
        - **email**: user email, only letters (a-z), numbers (0-9) and periods (.) are allowed, required
        - **password**: password, cannot be empty, required
        - **password_re_check**: password recheck, required
        - **role_id**: user role id, required
        - **faculty_id**: user faculty id, required

        **Return**: created user id
    """
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
        "message": f"Created user with id {last_record_id}",
        "code": http_status.HTTP_201_CREATED
    }


@users_router.delete("/{university_id}/users/",
                     name="delete_user",
                     response_model=JSENDOutSchema,
                     summary="Delete university user",
                     responses={
                         200: {"description": "Successful delete university user response"},
                         422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                     },
                     tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth=Depends(get_current_user)):
    query = delete(User).where(User.user_id == delete_user.user_id)

    await database.execute(query)

    return {
        "data": {
            "user_id": delete_user.user_id
        },
        "message": f"Deleted user with id {delete_user.user_id}",
        "code": http_status.HTTP_200_OK
    }


@users_router.post("/registration",
                   name="registration",
                   response_model=JSENDOutSchema[RegistrationOut],
                   summary="User registration",
                   responses={
                       200: {"description": "Successful user registration response"},
                       403: {"model": JSENDFailOutSchema, "description": "Registration time expired fail response"},
                       404: {"model": JSENDFailOutSchema, "description": "Invalid input data response"},
                       409: {"model": JSENDFailOutSchema, "description": "Input data already exist response"},
                       422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                   },
                   tags=["Authorization"])
async def registration(user: RegistrationIn):
    """
        **User registration**

        **Input**:
        - **token**: token from "Check user existence"
        - **email**: enter user email; only letters (a-z), numbers (0-9) and periods (.) are allowed
        - **password**: enter password; password cannot be empty

        **Return**: user id; faculty id; login, which consists of name and random number
    """
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

    transliterated_full_name = translit(
        full_name)  # TODO Local variable 'full_name' might be referenced before assignment
    login = f"{(transliterated_full_name[:4])}-{randint(100, 999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = insert(User).values(login=login, email=user.email, password=encoded_user_password, role_id=1,
                                is_active=True)
    last_record_id = await database.execute(query)

    query = update(Student).values(user_id=last_record_id).where(Student.student_id == student_id)
    await database.execute(query)

    query = insert(UserFaculty).values(user_id=last_record_id, faculty_id=faculty_id).returning(
        UserFaculty.faculty_id)  # TODO Local variable 'faculty_id' might be referenced before assignment
    user_faculty_data = await database.execute(query)

    return {
        "data": {
            "user_id": last_record_id,
            "faculty_id": user_faculty_data,
            "login": login
        },
        "message": f"User with id {last_record_id} was registered successfully",
        "code": http_status.HTTP_201_CREATED
    }


@users_router.post("/{university_id}/students/",
                   name="create_student",
                   response_model=JSENDOutSchema[CreateStudentOut],
                   summary="Create university student",
                   responses={
                       200: {"description": "Successful create student of the university response"},
                       422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                   },
                   tags=["Admin dashboard"])
# TODO after input id of the non-existent university it creates student
async def create_student(university_id: int, student: CreateStudentIn, auth=Depends(get_current_user)):
    """
        **Create university student**

        **Path**:
        - **university_id**: university id

        **Input**:
        - **full_name**: student fist name and last name, required
        - **telephone_number**: student telephone number, must consists of 12 digits, required
        - **course_id**: student course id, must be between 1 and 6, required
        - **faculty_id**: faculty id, required
        - **speciality_id**: speciality id, required
        - **gender**: student gender, 'Ч' or 'Ж'

        **Return**: created student id
    """
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
        "message": f"Created student {student.full_name}",
        "code": http_status.HTTP_201_CREATED
    }


@users_router.get("/{university_id}/students/",
                  name="read_students_list",
                  response_model=JSENDOutSchema[List[StudentsListOut]],
                  summary="Get university students list",
                  responses={
                      200: {"description": "Successful get all university students list response"},
                      422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                  },
                  tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(
    get_current_user)):  # TODO after input id of the non-existent university it returns the students
    if faculty_id:
        query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = select(students_list_view).where(students_list_view.c.university_id == university_id)

    return {
        "data": await database.fetch_all(query),
        "message": f"Got students list of the university with id {university_id}"
    }


@users_router.delete("/{university_id}/students/",
                     name="delete_student",
                     response_model=JSENDOutSchema,
                     summary="Delete university student",
                     responses={
                         200: {"description": "Successful delete university student response"},
                         422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                     },
                     tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    query = delete(Student).where(Student.student_id == delete_student.student_id)

    await database.execute(query)
    # TODO: in response key data has empty dict value, not like it's described
    return {
        "data": {
            "student_id": delete_student.student_id
        },
        "message": f"Deleted student with id {delete_student.student_id}",
        "code": http_status.HTTP_200_OK
    }


@users_router.get('/me',
                  name="read_me",
                  response_model=JSENDOutSchema[UserOut],
                  summary='Get current user info',
                  responses={200: {"description": "Successful get current user information response"}},
                  tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return {
        "data": user,
        "message": "Got current user information"
    }
