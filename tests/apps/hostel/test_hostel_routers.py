import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from typing import List

from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Faculty, Rector, University
from apps.hostel.models import Hostel
from apps.users.models import Student, User, UserFaculty
from tests.apps.conftest import assert_jsend_response
from tests.apps.educational_institution.factories import (
    FacultyFactory,
    RectorFactory,
    UniversityFactory,
)
from tests.apps.hostel.factories import HostelFactory, BedPlaceFactory
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
        hostels: List[Hostel] = HostelFactory.create_batch(size=3, university_id=university.university_id)
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
        amend = len(data) - 3
        for i in range(3):
            assert data[i+amend].get("university_id") == hostels[i].university_id
            assert data[i+amend].get("hostel_id") == hostels[i].hostel_id
            assert data[i+amend].get("number") == hostels[i].number
            assert data[i+amend].get("name") == hostels[i].name
            assert data[i+amend].get("city") == hostels[i].city
            assert data[i+amend].get("street") == hostels[i].street
            assert data[i+amend].get("build") == hostels[i].build
            assert data[i+amend].get("commandant_id") == hostels[i].commandant_id
            assert data[i+amend].get("commandant_full_name") == {
                'first_name': hostels[i].commandant.first_name,
                'last_name': hostels[i].commandant.last_name,
                'middle_name': hostels[i].commandant.middle_name,
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
        bed_places: List = BedPlaceFactory.create_batch(size=3)
        token: str = create_access_token(subject=user.email)
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_bed_places"
            ),
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
        amend = len(data) - 3
        for i in range(3):
            assert data[i+amend].get("bed_place_id") == bed_places[i].bed_place_id
            assert data[i+amend].get("bed_place_name") == bed_places[i].bed_place_name

