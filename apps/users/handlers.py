from apps.authorization.services import get_hashed_password
from apps.common.db import database
from apps.common.dependencies import get_async_session
from apps.common.exceptions import BackendException
from apps.users.models import User, user_list_view, Student, OneTimeToken, UserFaculty, students_list_view
from apps.users.schemas import UserOut, TokenPayload, CreateUserIn, DeleteUserIn, RegistrationIn, CreateStudentIn, \
    UserIn, DeleteStudentIn, StudentCheckExistanceIn
from apps.users.serivces import(
    get_login, get_student_attr, get_token_data, get_login_full_name, get_token_and_expires, user_service,
    user_list_service
)
from settings import Settings

from datetime import datetime
from fastapi import Depends, HTTPException, Request, status as http_status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union


class UserHandler:

    async def check_student(
            self,
            *,
            request: Request,
            student: StudentCheckExistanceIn):
        query = select(Student).where(Student.full_name == student.full_name,
                                      Student.telephone_number == student.telephone_number)
        result = await database.fetch_one(query)
        if not result:
            raise BackendException(
                message="Student data was not found. Please, try again.",
                code=http_status.HTTP_404_NOT_FOUND
            )

        student_id = result.student_id

        token, expires = get_token_and_expires()

        query = insert(OneTimeToken).values(student_id=student_id, token=token,
                                            expires=expires).returning(OneTimeToken.token_id)
        last_record_id = await database.execute(query)
        query = select(OneTimeToken).where(OneTimeToken.token_id == last_record_id)
        return await database.fetch_one(query)

    async def read_users_list(university_id: int):
        query = select(user_list_view).where(user_list_view.c.university_id == university_id)
        return await database.fetch_all(query)

    async def create_user(user: CreateUserIn):
        CreateUserIn(
            email=user.email,
            password=user.password,
            password_re_check=user.password_re_check,
            role_id=user.role_id,
            faculty_id=user.faculty_id
        )

        hashed_password = get_hashed_password(user.password)

        query = insert(User).values(login=get_login(user.email), password=hashed_password,
                                    email=user.email, role_id=user.role_id,
                                    is_active=False)

        last_record_id = await database.execute(query)

        for faculty_id in user.faculty_id:
            query = insert(UserFaculty).values(user_id=last_record_id,
                                               faculty_id=faculty_id)
            await database.execute(query)

        return last_record_id

    async def del_user(delete_user: DeleteUserIn):
        query = delete(User).where(User.user_id == delete_user.user_id)
        await database.execute(query)

    async def registration(user: RegistrationIn):
        RegistrationIn(
            token=user.token,
            email=user.email,
            password=user.password,
            password_re_check=user.password_re_check)

        query = select(OneTimeToken).where(OneTimeToken.token == user.token)

        token_data = await database.fetch_all(query)

        expires, student_id = get_token_data(token_data)

        query = select(Student).where(Student.student_id == student_id)

        student = await database.fetch_all(query)

        full_name, faculty_id = get_student_attr(student)

        login = get_login_full_name(full_name)

        # Encoding password
        encoded_user_password = get_hashed_password(user.password)

        query = insert(User).values(login=login, email=user.email, password=encoded_user_password, role_id=1,
                                    is_active=True)
        last_record_id = await database.execute(query)

        query = update(Student).values(user_id=last_record_id).where(Student.student_id == student_id)
        await database.execute(query)

        query = insert(UserFaculty).values(
            user_id=last_record_id,
            faculty_id=faculty_id
        ).returning(UserFaculty.faculty_id)
        user_faculty_data = await database.execute(query)

        return {
            "user_id": last_record_id,
            "faculty_id": user_faculty_data,
            "login": login
        }

    async def create_student(student: CreateStudentIn):
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

        return {"student_id": student_id}

    async def read_students_list(university_id: int, faculty_id: Union[
        int, None] = None):  # TODO after input id of the non-existent university it returns the students
        if faculty_id:
            query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
        else:
            query = select(students_list_view).where(students_list_view.c.university_id == university_id)
        return await database.fetch_all(query)

    async def delete_student(del_student: DeleteStudentIn):
        query = delete(Student).where(Student.student_id == del_student.student_id)

        await database.execute(query)
        # TODO: in response key data has empty dict value, not like it's discribed

    async def get_me(user: UserIn = Depends(get_current_user)):
        return {
            "data": user,
            "message": "Got user information"
        }


user_handler = UserHandler()
