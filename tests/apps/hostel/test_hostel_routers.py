from typing import List

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient

from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Faculty, Rector, University
from apps.hostel.models import BedPlace, Hostel
from apps.users.models import Student, User, UserFaculty
from tests.apps.conftest import assert_jsend_response, find_created_instance
from tests.apps.educational_institution.factories import (
    FacultyFactory,
    RectorFactory,
    UniversityFactory,
)
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory
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
        hostels: List[Hostel] = HostelFactory.create_batch(
            size=3, university_id=university.university_id
        )
        faculty: Faculty = FacultyFactory(university_id=university.university_id)
        mod_email = faker.email()
        user: User = UserFactory(mod_email=mod_email)
        user_faculty: UserFaculty = UserFacultyFactory(
            user_id=user.user_id, faculty_id=faculty.faculty_id
        )
        student: Student = StudentFactory(
            user_id=user.user_id, faculty_id=faculty.faculty_id
        )
        token: str = create_access_token(subject=user.email)
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_university_hostels", university_id=university.university_id
            ),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got hostels list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]

        for hostel in hostels:
            created_instance = find_created_instance(
                hostel.hostel_id, data, "hostel_id"
            )
            assert created_instance.get("university_id") == hostel.university_id
            assert created_instance.get("hostel_id") == hostel.hostel_id
            assert created_instance.get("number") == hostel.number
            assert created_instance.get("name") == hostel.name
            assert created_instance.get("city") == hostel.city
            assert created_instance.get("street") == hostel.street
            assert created_instance.get("build") == hostel.build
            assert created_instance.get("commandant_id") == hostel.commandant_id
            assert created_instance.get("commandant_full_name") == {
                "first_name": hostel.commandant.first_name,
                "last_name": hostel.commandant.last_name,
                "middle_name": hostel.commandant.middle_name,
            }

    @pytest.mark.asyncio
    async def test_read_hostel_list_404_only(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
    ) -> None:
        token: str = create_access_token(subject="ass@a.com")
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_university_hostels", university_id="24"
            ),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_404_NOT_FOUND,
            status=JSENDStatus.FAIL,
            message="User not found",
            code=status.HTTP_404_NOT_FOUND,
        )

    @pytest.mark.asyncio
    async def test_read_hostel_list_401_only(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
    ) -> None:
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_university_hostels", university_id="25"
            )
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_401_UNAUTHORIZED,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=status.HTTP_401_UNAUTHORIZED,
        )
        assert response.json()["data"] == "Not authenticated"


class TestReadBedPlaceRouter:
    @pytest.mark.asyncio
    async def test_read_bed_place_200_only(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
    ) -> None:
        mod_email = faker.email()
        user: User = UserFactory(mod_email=mod_email)
        bed_places: List[BedPlace] = BedPlaceFactory.create_batch(size=3)
        token: str = create_access_token(subject=user.email)
        response = await async_client.get(
            url=app_fixture.url_path_for(name="read_bed_places"),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got available bed places list",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]

        for bed_place in bed_places:
            created_instance = find_created_instance(
                bed_place.bed_place_id, data, "bed_place_id"
            )
            assert created_instance.get("bed_place_id") == bed_place.bed_place_id
            assert created_instance.get("bed_place_name") == bed_place.bed_place_name
