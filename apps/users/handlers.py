from apps.authorization.services import get_hashed_password
from apps.common.exceptions import BackendException
from apps.common.utils import (add_random_digits_and_cut_username, get_student_attr, get_token_data,
                               get_generated_username, get_token_and_expires)
from apps.users.schemas import (CreateUserIn, DeleteUserIn, RegistrationIn, CreateStudentIn,
                                DeleteStudentIn, StudentCheckExistenceIn)
from apps.services.services import user_faculty_service
from apps.users.services import (student_service, one_time_token_service, student_list_service,
                                 user_list_service, user_service)

from fastapi import Request, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class UserHandler:

    async def check_student(
            self,
            *,
            request: Request,
            student: StudentCheckExistenceIn,
            session: AsyncSession):     # TODO Refactor this method
        result = await student_service.read(session=session, obj=student)
        if not result:
            raise BackendException(
                message="Student data was not found. Please, try again.",
                code=http_status.HTTP_404_NOT_FOUND
            )
        token, expires = get_token_and_expires()

        one_time_token = await one_time_token_service.create(
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
            session: AsyncSession):     # TODO refactor this method
        hashed_password = get_hashed_password(user.password)
        created_user = await user_service.create(
            session=session,
            data={
                "login": add_random_digits_and_cut_username(user.email),
                "password": hashed_password,
                "email": user.email,
                "role_id": user.role_id,
                "is_active": False
            })
        for faculty_id in user.faculty_id:
            await user_faculty_service.create(
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
        await user_service.delete(session=session, obj=delete_user)

    async def registration(
            self,
            *,
            request: Request,
            user: RegistrationIn,
            session: AsyncSession):
        token_data = await one_time_token_service.read(session=session, data={"token": user.token})
        expires, student_id = get_token_data(token_data)
        student = await student_service.read(session=session, data={"student_id": student_id})
        first_name, last_name, faculty_id = get_student_attr(student)
        login = get_generated_username(last_name, first_name)
        # Encoding password
        encoded_user_password = get_hashed_password(user.password)
        registered_user = await user_service.create(
            session=session,
            data={
                "login": login,
                "email": user.email,
                "password": encoded_user_password,
                "role_id": 1,
                "is_active": True
            })
        await student_service.update(
            session=session,
            data={"student_id": student_id},
            obj={"user_id": registered_user.user_id}
        )
        user_faculty_data = await user_faculty_service.create(
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
        created_student = await student_service.create(
            session=session,
            obj=student
        )
        return {"student_id": created_student.student_id}

    async def read_students_list(
            self,
            *,
            request: Request,
            university_id: int,
            faculty_id: Optional[int] = None,
            session: AsyncSession):  # TODO after input id of the non-existent university it returns the students
        filters = {"university_id": university_id}
        if faculty_id:
            filters["faculty_id"] = faculty_id
        return await student_list_service.list(
            session=session,
            filters=filters
        )

    async def delete_student(
            self,
            *,
            request: Request,
            del_student: DeleteStudentIn,
            session: AsyncSession):
        await student_service.delete(session=session, obj=del_student)
        # TODO: in response key data has empty dict value, not like it's discribed


user_handler = UserHandler()
