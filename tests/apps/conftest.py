import typing
import uuid
from typing import List, Tuple

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient, Response

from apps.authorization.services import create_access_token
from apps.common.enums import JSENDStatus
from apps.common.services import AsyncCRUDBase, ModelType
from apps.educational_institutions.models import Dean, Faculty, Speciality, University
from apps.services.models import Status
from apps.users.models import Student, User
from tests.apps.educational_institution.factories import (
    FacultyFactory,
    SpecialityFactory,
    UniversityFactory,
)
from tests.apps.services.factories import StatusFactory
from tests.apps.users.factories import StudentFactory, UserFactory, UserFacultyFactory


def assert_jsend_response(
    response: Response,
    http_code: status,
    status: JSENDStatus,
    message: str,
    code: int,
    data: typing.Any = ...,
) -> None:
    response_json = response.json()
    assert response.status_code == http_code
    assert response_json["status"] == status
    assert response_json["message"] == message
    assert response_json["code"] == code
    if data is not ...:
        assert response_json["data"] == data


@pytest.fixture(scope="function")
async def access_token(
    faker: Faker,
) -> str:
    user: User = UserFactory(mod_email=faker.email())
    return create_access_token(subject=user.email)


@pytest.fixture(scope="function")
async def student_creation(
    faker: Faker,
) -> Tuple[str, University, User, Student, Faculty, Speciality]:
    user: User = UserFactory(mod_email=faker.email())
    university: University = UniversityFactory()
    faculty: Faculty = FacultyFactory(university_id=university.university_id)
    request_status_list: List[Status] = StatusFactory.create_batch(size=10)
    speciality: Speciality = SpecialityFactory(faculty_id=faculty.faculty_id)
    UserFacultyFactory(user_id=user.user_id, faculty_id=faculty.faculty_id)
    student: Student = StudentFactory(
        user_id=user.user_id,
        speciality_id=speciality.speciality_id,
        faculty_id=faculty.faculty_id,
        gender="M",
    )
    token = create_access_token(subject=user.email)
    return token, university, user, student, faculty, speciality


def find_created_instance(
    instance_attr: typing.Any, data: List, attr_name: str
) -> ModelType:
    for instance in data:
        if instance.get(attr_name) == instance_attr:
            return instance


status_service = AsyncCRUDBase(model=Status)
dean_service = AsyncCRUDBase(model=Dean)
speciality_service = AsyncCRUDBase(model=Speciality)
