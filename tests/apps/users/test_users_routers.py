import datetime
from typing import List, Tuple

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.models import Role
from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.common.utils import get_token_and_expires_at
from apps.educational_institutions.models import Faculty, Rector, University, Speciality
from apps.hostel.models import BedPlace, Hostel
from apps.users.models import Student, User, UserFaculty
from apps.users.services import one_time_token_service
from tests.apps.authorization.factories import RoleFactory
from tests.apps.conftest import assert_jsend_response, find_created_instance
from tests.apps.educational_institution.factories import (
    FacultyFactory,
    RectorFactory,
    UniversityFactory,
)
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory
from tests.apps.users.factories import StudentFactory, UserFactory, UserFacultyFactory


class TestCreateStudentExistence:
    async def test_create_student_existence_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            db_session: AsyncSession,
    ) -> None:
        student: Student = StudentFactory(
            user_id=None, telephone_number="333333333333"
        )
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for("create_student_existence"),
            json={
                "last_name": student.last_name,
                "first_name": student.first_name,
                "telephone_number": student.telephone_number,
            }
        )
        one_time_token = await one_time_token_service.read(
            session=db_session, data={"student_id": student.student_id}
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Get information of student with id {student.student_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("student_id") == student.student_id
        assert data.get("token") == one_time_token.token
        assert data.get("expires_at") == (
                one_time_token.expires_at.strftime("%Y-%m-%d")
                + "T"
                + one_time_token.expires_at.strftime("%H:%M:%S.%f")
                + "+00:00"
        )

    async def test_create_student_existence_422(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            db_session: AsyncSession,
    ) -> None:
        student: Student = StudentFactory(
            user_id=None, telephone_number="333333333333"
        )
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for("create_student_existence"),
            json={
                "last_name": student.last_name,
                "first_name": student.first_name,
                "telephone_number": faker.pyint(),
            }
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestReadUsersList:
    async def test_read_users_list_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            access_token: str,
    ) -> None:
        token = access_token
        university: University = UniversityFactory()
        faculties: List[Faculty] = FacultyFactory.create_batch(
            size=5, university_id=university.university_id
        )
        users: List[User] = UserFactory.create_batch(size=5)
        user_faculties = [
            UserFacultyFactory(
                user_id=users[i].user_id, faculty_id=faculties[i].faculty_id
            ) for i in range(5)
        ]
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_users_list",
                university_id=university.university_id,
            ),
            headers={"Authorization": f"Bearer {token}"}
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got user list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        for user in users:
            created_instance = find_created_instance(
                user.user_id, data, "user_id"
            )
            assert created_instance.get("user_id") == user.user_id
            assert created_instance.get("login") == user.login
            assert created_instance.get("last_visit_at") == (
                user.last_visit_at.strftime("%Y-%m-%d")
                + "T"
                + user.last_visit_at.strftime("%H:%M:%S")
                + "+00:00"
            )
            assert created_instance.get("email") == user.email
            assert created_instance.get("is_active") == user.is_active
            assert created_instance.get("role") == [{
                "role": user.roles.role_id,
                "role_name": user.roles.role_name,
            }]
            user_faculty_set = {
                faculty.faculty_id for faculty in user_faculties
                if faculty.user_id == user.user_id
            }
            assert created_instance.get("faculties") == [
                {
                    "faculty": faculty.faculty_id,
                    "faculty_name": faculty.name
                } for faculty in faculties if faculty.faculty_id in user_faculty_set
            ]
            assert created_instance.get("university_id") == university.university_id


class TestCreateUser:
    async def test_create_user_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            access_token: str,
    ) -> None:
        university: University = UniversityFactory()
        faculties: List[Faculty] = FacultyFactory.create_batch(
            size=2, university_id=university.university_id
        )
        role: Role = RoleFactory()
        token = access_token
        email = faker.email()
        password = faker.pystr(min_chars=8, max_chars=50)
        response = await async_client.request(
            method="POsT",
            url=app_fixture.url_path_for(
                name="create_user",
                university_id=university.university_id,
            ),
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": email,
                "password": password,
                "password_re_check": password,
                "role_id": role.role_id,
                "faculty_id": [faculty.faculty_id for faculty in faculties],
            },
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Created user with id {data.get('user_id')}",
            code=status.HTTP_200_OK,
        )
        assert data.get("login")[-3:].isdigit()
        assert data.get("last_visit")[:10] == datetime.datetime.utcnow().strftime("%Y-%m-%d")
        assert data.get("email") == email
        assert data.get("is_active") is False
        assert data.get("role_id") == role.role_id


class TestDeleteUser:
    async def test_delete_user_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            access_token: str,
    ) -> None:
        token = access_token
        university: University = UniversityFactory()
        user: User = UserFactory()
        response = await async_client.request(
            method="DELETE",
            url=app_fixture.url_path_for(
                name="delete_user",
                university_id=university.university_id,
            ),
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user.user_id},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Deleted user with id {user.user_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("user_id") == user.user_id
