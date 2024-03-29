from typing import List, Optional

from fastapi import Request
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.services import get_hashed_password
from apps.common.exceptions import BackendException
from apps.common.utils import (
    add_random_digits_and_cut_username,
    get_generated_username,
    get_student_attr,
    get_token_and_expires_at,
    get_token_data,
)
from apps.services.services import user_faculty_service
from apps.users.schemas import (
    CreateStudentIn,
    CreateStudentOut,
    CreateUserIn,
    CreateUserOut,
    DeleteStudentIn,
    DeleteUserIn,
    RegistrationIn,
    StudentCheckExistenceIn,
    StudentCheckExistenceOut,
    StudentsListOut,
    UsersListViewOut,
)
from apps.users.services import (
    one_time_token_service,
    student_list_service,
    student_service,
    user_list_service,
    user_service,
)


class UserHandler:
    @staticmethod
    async def check_student(
        *, request: Request, student: StudentCheckExistenceIn, session: AsyncSession
    ) -> StudentCheckExistenceOut:  # TODO Refactor this method
        result = await student_service.read(session=session, obj=student)
        if not result:
            raise BackendException(
                message="Student data was not found. Please, try again.",
                code=http_status.HTTP_404_NOT_FOUND,
            )
        token, expires_at = get_token_and_expires_at()

        one_time_token = await one_time_token_service.create(
            session=session,
            data={
                "student_id": result.student_id,
                "token": token,
                "expires_at": expires_at,
            },
        )
        return one_time_token

    @staticmethod
    async def read_users_list(
        *, request: Request, university_id: int, session: AsyncSession
    ) -> List[UsersListViewOut]:
        return await user_list_service.list(
            session=session, filters={"university_id": university_id}
        )

    @staticmethod
    async def create_user(
        *, request: Request, user: CreateUserIn, session: AsyncSession
    ) -> CreateUserOut:  # TODO refactor this method
        hashed_password = get_hashed_password(user.password)
        created_user = await user_service.create(
            session=session,
            data={
                "login": add_random_digits_and_cut_username(user.email),
                "password": hashed_password,
                "email": user.email,
                "role_id": user.role_id,
                "is_active": False,
            },
        )
        for faculty_id in user.faculty_id:
            await user_faculty_service.create(
                session=session,
                data={"user_id": created_user.user_id, "faculty_id": faculty_id},
            )
        return CreateUserOut(
            user_id=created_user.user_id,
            login=created_user.login,
            last_visit=created_user.last_visit_at,
            email=created_user.email,
            is_active=created_user.is_active,
            role_id=created_user.role_id,
        )

    @staticmethod
    async def del_user(
        *, request: Request, delete_user: DeleteUserIn, session: AsyncSession
    ) -> None:
        await user_service.delete(session=session, obj=delete_user)

    @staticmethod
    async def registration(
        *, request: Request, user: RegistrationIn, session: AsyncSession
    ) -> CreateUserOut:
        token_data = await one_time_token_service.read(
            session=session, data={"token": user.token}
        )
        expires_at, student_id = get_token_data(token_data)
        student = await student_service.read(
            session=session, data={"student_id": student_id}
        )
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
                "is_active": True,
            },
        )
        await student_service.update(
            session=session,
            data={"student_id": student_id},
            obj={"user_id": registered_user.user_id},
        )
        await user_faculty_service.create(
            session=session,
            data={"user_id": registered_user.user_id, "faculty_id": faculty_id},
        )
        return CreateUserOut(
            user_id=registered_user.user_id,
            login=registered_user.login,
            last_visit_at=registered_user.last_visit_at,
            email=registered_user.email,
            is_active=registered_user.is_active,
            role_id=registered_user.role_id,
        )

    @staticmethod
    async def create_student(
        *, request: Request, student: CreateStudentIn, session: AsyncSession
    ) -> CreateStudentOut:
        return await student_service.create(
            session=session,
            obj=student,
        )

    @staticmethod
    async def read_students_list(
        *,
        request: Request,
        university_id: int,
        faculty_id: Optional[int] = None,
        session: AsyncSession
    ) -> List[
        StudentsListOut
    ]:  # TODO after input id of the non-existent university it returns the students
        filters = {"university_id": university_id}
        if faculty_id:
            filters["faculty_id"] = faculty_id
        return await student_list_service.list(session=session, filters=filters)

    @staticmethod
    async def delete_student(
        *, request: Request, del_student: DeleteStudentIn, session: AsyncSession
    ) -> None:
        await student_service.delete(session=session, obj=del_student)
        # TODO: in response key data has empty dict value, not like it's described


user_handler = UserHandler()
