from typing import List, Tuple

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.common.utils import get_token_and_expires_at
from apps.educational_institutions.models import Faculty, Rector, University, Speciality
from apps.hostel.models import BedPlace, Hostel
from apps.users.models import Student, User, UserFaculty
from apps.users.services import one_time_token_service
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
