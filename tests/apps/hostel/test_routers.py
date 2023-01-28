import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Course, Faculty, Rector, University
from apps.hostel.routers import hostel_router
from apps.users.models import Student, User, UserFaculty
from apps.users.services import user_service
from tests.apps.conftest import assert_jsend_response
from tests.apps.educational_institution.factories import (
    CourseFactory,
    FacultyFactory,
    RectorFactory,
    UniversityFactory,
)
from tests.apps.users.factories import StudentFactory, UserFactory, UserFacultyFactory


class TestReadHostelListRouter:
    @pytest.mark.asyncio
    async def test_read_hostel_list_200_only(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
    ) -> None:
        rector: Rector = RectorFactory()
        university: University = UniversityFactory(rector_id=rector.rector_id)
        faculty: Faculty = FacultyFactory(university_id=university.university_id)
        user: User = UserFactory(email="a@a.com")
        user_faculty: UserFaculty = UserFacultyFactory(
            user_id=user.user_id, faculty_id=faculty.faculty_id
        )
        student: Student = StudentFactory(
            user_id=user.user_id, faculty_id=faculty.faculty_id
        )
        token: str = create_access_token(subject="a@a.com")
        response = await async_client.get(
            url=f"/{university.university_id}/hostels/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got hostels list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
