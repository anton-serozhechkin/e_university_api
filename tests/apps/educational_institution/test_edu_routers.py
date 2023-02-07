from typing import List

from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Course, Dean, Faculty, University
from tests.apps.conftest import (
    assert_jsend_response,
    dean_service,
    find_created_instance,
)
from tests.apps.educational_institution.factories import (
    CourseFactory,
    DeanFactory,
    FacultyFactory,
    SpecialityFactory,
    UniversityFactory,
)


class TestReadFacultyList:
    async def test_read_faculty_list_200(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        access_token: str,
    ) -> None:
        university: University = UniversityFactory()
        faculties: List[Faculty] = FacultyFactory.create_batch(
            size=3, university_id=university.university_id
        )
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_faculty_list", university_id=university.university_id
            ),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got faculty list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]

        for faculty in faculties:
            created_instance = find_created_instance(
                faculty.faculty_id, data, "faculty_id"
            )
            assert created_instance.get("name") == faculty.name
            assert created_instance.get("shortname") == faculty.shortname
            assert created_instance.get("main_email") == faculty.main_email
            assert created_instance.get("dean_id") == faculty.dean_id
            assert created_instance.get("dean_full_name") == {
                "first_name": faculty.dean.first_name,
                "last_name": faculty.dean.last_name,
                "middle_name": faculty.dean.middle_name,
            }


class TestCreateFaculty:
    async def test_create_faculty_200_exist_dean(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        access_token: str,
    ) -> None:
        university: University = UniversityFactory()
        dean: Dean = DeanFactory()
        faculty_name = faker.pystr(max_chars=255, min_chars=10)
        faculty_short_name = faker.pystr(max_chars=20, min_chars=2)
        faculty_email = faker.email()
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_faculty", university_id=university.university_id
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
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
                "dean_last_name": "",
                "dean_first_name": "",
                "dean_middle_name": "",
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
        assert (
            data.get("dean_full_name") is None
        )  # TODO Must be changed after changing handler behaviour

    async def test_create_faculty_200_new_dean(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        db_session: AsyncSession,
        access_token: str,
    ) -> None:
        university: University = UniversityFactory()
        faculty_name = faker.pystr(max_chars=255, min_chars=10)
        faculty_short_name = faker.pystr(max_chars=20, min_chars=2)
        faculty_email = faker.email()
        dean_last_name = faker.last_name()
        dean_first_name = faker.first_name()
        dean_middle_name = faker.first_name()
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_faculty", university_id=university.university_id
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "university_id": university.university_id,
                "name": faculty_name,
                "shortname": faculty_short_name,
                "main_email": faculty_email,
                "dean_id": None,
                "dean_last_name": dean_last_name,
                "dean_first_name": dean_first_name,
                "dean_middle_name": dean_middle_name,
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
        dean = await dean_service.read(
            session=db_session,
            data={"last_name": dean_last_name, "first_name": dean_first_name},
        )
        assert data.get("university_id") == university.university_id
        assert data.get("name") == faculty_name
        assert data.get("shortname") == faculty_short_name
        assert data.get("main_email") == faculty_email
        assert data.get("dean_id") == dean.dean_id
        assert (
            data.get("dean_full_name") is None
        )  # TODO Must be changed after changing handler behaviour

    async def test_create_faculty_422(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        access_token: str,
    ) -> None:
        fake_email = faker.pystr(max_chars=15)
        university: University = UniversityFactory()
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_faculty", university_id=university.university_id
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "university_id": university.university_id,
                "name": faker.pystr(),
                "shortname": faker.pystr(),
                "main_email": fake_email,
                "dean_id": 1,
                "dean_last_name": "",
                "dean_first_name": "",
                "dean_middle_name": "",
            },
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestReadSpecialityList:
    async def test_read_speciality_list_200(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        access_token: str,
    ) -> None:
        university: University = UniversityFactory()
        faculties: List[Faculty] = FacultyFactory.create_batch(
            size=3, university_id=university.university_id
        )
        specialities = [
            SpecialityFactory(faculty_id=faculty.faculty_id) for faculty in faculties
        ]
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_speciality_list",
                university_id=university.university_id,
            ),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Got speciality list of the university with id {university.university_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]

        for speciality in specialities:
            created_instance = find_created_instance(
                speciality.speciality_id, data, "speciality_id"
            )
            assert created_instance.get("university_id") == university.university_id
            assert created_instance.get("faculty_id") == speciality.faculty_id
            assert created_instance.get("speciality_info") == {
                "code": speciality.code,
                "full_name": speciality.name,
            }


class TestReadCourseList:
    async def test_read_course_list_200(
        self,
        async_client: AsyncClient,
        app_fixture: FastAPI,
        faker: Faker,
        access_token: str,
    ) -> None:
        courses: List[Course] = CourseFactory.create_batch(size=3)
        response = await async_client.get(
            url=app_fixture.url_path_for("read_courses_list"),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got all courses",
            code=status.HTTP_200_OK,
        )
        for course in courses:
            created_instance = find_created_instance(
                course.course_id, data, "course_id"
            )
            assert created_instance.get("value") == course.value
