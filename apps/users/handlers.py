from apps.authorization.services import get_hashed_password
from apps.common.db import database
from apps.common.dependencies import get_async_session
from apps.common.exceptions import BackendException
from apps.users.models import User, user_list_view, Student, OneTimeToken, UserFaculty, students_list_view
from apps.users.schemas import UserOut, TokenPayload, CreateUserIn, DeleteUserIn, RegistrationIn, CreateStudentIn, \
    UserIn, DeleteStudentIn, StudentCheckExistanceIn
from apps.services.services import user_faculty_service
from apps.users.serivces import(
    get_login, get_student_attr, get_token_data, get_login_full_name, get_token_and_expires, student_service,
    one_time_token_service, user_list_service, user_service
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
            student: StudentCheckExistanceIn,
            session: AsyncSession):
        result = await student_service.read_mod(session=session, data={}, schema=student)
        if not result:
            raise BackendException(
                message="Student data was not found. Please, try again.",
                code=http_status.HTTP_404_NOT_FOUND
            )
        token, expires = get_token_and_expires()

        one_time_token = await one_time_token_service.create_mod(
            session=session,
            data={
                "student_id": result.student_id,
                "token": token,
                "expires": expires
            })
        return one_time_token

    async def read_users_list(
            self,
            *,
            request: Request,
            university_id: int,
            session: AsyncSession):
        return await user_list_service.list(session=session, filters={"university_id": university_id})

    async def create_user(
            self,
            *,
            request: Request,
            user: CreateUserIn,
            session: AsyncSession):
        CreateUserIn(
            email=user.email,
            password=user.password,
            password_re_check=user.password_re_check,
            role_id=user.role_id,
            faculty_id=user.faculty_id
        )
        hashed_password = get_hashed_password(user.password)
        created_user = await user_service.create_mod(
            session=session,
            data={
                "login": get_login(user.email),
                "password": hashed_password,
                "email": user.email,
                "role_id": user.role_id,
                "is_active": False
            })
        for faculty_id in user.faculty_id:
            await user_faculty_service.create_mod(
                session=session,
                data={"user_id": created_user.user_id,
                      "faculty_id": faculty_id})
        return created_user.user_id

    async def del_user(
            self,
            *,
            request: Request,
            delete_user: DeleteUserIn,
            session: AsyncSession):
        await user_service.delete(session=session, data={}, schema=delete_user)

    async def registration(
            self,
            *,
            request: Request,
            user: RegistrationIn,
            session: AsyncSession):
        token_data = await one_time_token_service.read_mod(session=session, data={"token": user.token})
        expires, student_id = get_token_data(token_data)
        student = await student_service.read_mod(session=session, data={"student_id": student_id})
        full_name, faculty_id = get_student_attr(student)
        login = get_login_full_name(full_name)
        # Encoding password
        encoded_user_password = get_hashed_password(user.password)
        registered_user = await user_service.create_mod(
            session=session,
            data={
                "login": login,
                "email": user.email,
                "password": encoded_user_password,
                "role_id": 1,
                "is_active": True
            })
        await student_service.update_mod(
            session=session,
            data={"student_id": student_id},
            obj={"user_id": registered_user.user_id}
        )
        user_faculty_data = await user_faculty_service.create_mod(
            session=session,
            data={
                "user_id": registered_user.user_id,
                "faculty_id": faculty_id
            })
        return {
            "user_id": registered_user.user_id,
            "faculty_id": user_faculty_data.user_id,
            "login": login
        }

    async def create_student(
            self,
            *,
            request: Request,
            student: CreateStudentIn,
            session: AsyncSession):
        created_student = await student_service.create_mod(
            session=session,
            data={},
            schema=student
        )
        return {"student_id": created_student.student_id}

    async def read_students_list(
            self,
            *,
            request: Request,
            university_id: int,
            faculty_id: Union[int, None] = None,
            session: AsyncSession):  # TODO after input id of the non-existent university it returns the students
        if faculty_id:
            query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
        else:
            query = select(students_list_view).where(students_list_view.c.university_id == university_id)
        return await database.fetch_all(query)

    async def delete_student(
            self,
            *,
            request: Request,
            del_student: DeleteStudentIn,
            session: AsyncSession):
        query = delete(Student).where(Student.student_id == del_student.student_id)

        await database.execute(query)
        # TODO: in response key data has empty dict value, not like it's discribed

    # async def get_me(user: UserIn = Depends(get_current_user)):
    #     return {
    #         "data": user,
    #         "message": "Got user information"
    #     }


user_handler = UserHandler()
