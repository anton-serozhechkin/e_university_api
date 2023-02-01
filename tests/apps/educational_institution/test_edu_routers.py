import json

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from typing import List

from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Faculty, Rector, University, Dean
from apps.hostel.models import Hostel
from apps.users.models import Student, User, UserFaculty
from tests.apps.conftest import assert_jsend_response
from tests.apps.educational_institution.factories import (
    FacultyFactory,
    RectorFactory,
    UniversityFactory,
    DeanFactory,
)
from tests.apps.hostel.factories import HostelFactory, BedPlaceFactory
from tests.apps.users.factories import StudentFactory, UserFactory, UserFacultyFactory


class TestReadFacultyList:
    async def test_read_faculty_list_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
    ) -> None:
        mod_email = faker.email()
        user: User = UserFactory(mod_email=mod_email)
        university: University = UniversityFactory()
        faculties: List[Faculty] = FacultyFactory.create_batch(
            size=3, university_id=university.university_id
        )
        token: str = create_access_token(subject=user.email)
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_faculty_list", university_id=university.university_id
            ),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got faculty list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        amend = len(data) - 3
        for i in range(3):
            assert data[i+amend].get("name") == faculties[i].name
            assert data[i+amend].get("shortname") == faculties[i].shortname
            assert data[i+amend].get("main_email") == faculties[i].main_email
            assert data[i+amend].get("dean_id") == faculties[i].dean_id
            assert data[i+amend].get("dean_full_name") == {
                "first_name": faculties[i].dean.first_name,
                "last_name": faculties[i].dean.last_name,
                "middle_name": faculties[i].dean.middle_name,
            }


class TestCreateFaculty:
    async def test_create_faculty_200_exist_dean(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
    ):
        mod_email = faker.email()
        user: User = UserFactory(mod_email=mod_email)
        university: University = UniversityFactory()
        dean: Dean = DeanFactory()
        token = create_access_token(subject=user.email)
        faculty_name = faker.pystr(max_chars=255, min_chars=10)
        faculty_short_name = faker.pystr(max_chars=20, min_chars=2)
        faculty_email = faker.email()
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(name="create_faculty", university_id=university.university_id),
            headers={
                "Authorization": f'Bearer {token}',
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "university_id": university.university_id,
                "name": faculty_name,
                "shortname": faculty_short_name,
                "main_email": faculty_email,
                "dean_id": dean.dean_id,
                "dean_last_name": '',
                "dean_first_name": '',
                "dean_middle_name": '',
            },
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f'Successfully created faculty with id {data.get("faculty_id")}',
            code=status.HTTP_200_OK,
        )
        assert data.get("university_id") == university.university_id
        assert data.get("name") == faculty_name
        assert data.get("shortname") == faculty_short_name
        assert data.get("main_email") == faculty_email
        assert data.get("dean_id") == dean.dean_id
        assert data.get("dean_full_name") is None # TODO Must be changed after changing handler behaviour
