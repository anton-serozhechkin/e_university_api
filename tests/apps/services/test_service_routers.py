from typing import Tuple
import datetime
import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import json

from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Faculty, University, Speciality
from apps.hostel.models import Hostel, BedPlace
from apps.services.models import Service, UserRequest, UserRequestReview
from apps.services.schemas import UserRequestReviewIn
from apps.users.models import Student, User, UserFaculty
from tests.apps.conftest import assert_jsend_response, find_created_instance, status_service
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory
from tests.apps.services.factories import ServiceFactory, UserRequestFactory, StatusFactory, UserRequestReviewFactory
from tests.apps.users.factories import StudentFactory, UserFactory, UserFacultyFactory


class TestCheckUserRequestExistence:
    async def test_check_user_request_existence_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        service: Service = ServiceFactory()
        request_status = await status_service.read(
            session=db_session, data={"status_id": 3}
        )
        user_request: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id,
        )
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_existence",
                university_id=university.university_id,
                service_id=service.service_id
            ),
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got user request existence",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("user_request_id") == user_request.user_request_id
        assert data.get("user_request_exist") is True
        assert data.get("status") == {
            "status_id": request_status.status_id,
            "status_name": request_status.status_name,
        }

    async def test_check_user_request_existence_200_empty(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_existence",
                university_id=university.university_id,
                service_id=faker.pyint(min_value=9000),
            ),
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got user request existence",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("user_request_id") is None
        assert data.get("user_request_exist") is False
        assert data.get("status") is None


class TestReadUserRequestList:
    async def test_read_user_request_list_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        request_status = await status_service.read(
            session=db_session, data={"status_id": 3}
        )
        service_1: Service = ServiceFactory()
        service_2: Service = ServiceFactory()
        user_request_1: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service_1.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id,
        )
        user_request_2: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service_2.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id,
        )
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_list",
                university_id=university.university_id,
            ),
            headers={
                "Authorization": f"Bearer {token}"
            },
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got user requests list",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        for user_request in [user_request_1, user_request_2]:
            created_instance = find_created_instance(
                user_request.user_request_id, data, "user_request_id"
            )
            assert created_instance.get("university_id") == user_request.university_id
            assert created_instance.get("user_id") == user_request.user_id
            assert created_instance.get("user_request_id") == user_request.user_request_id
            assert created_instance.get("service_name") == user_request.service.service_name
            assert created_instance.get("created_at") == (
                user_request.created_at.strftime('%Y-%m-%d')
                + 'T' + user_request.created_at.strftime('%H:%M:%S') + '+00:00'
            )
            assert created_instance.get("status") == {
                "status_id": user_request.status_id,
                "status_name": request_status.status_name,
            }


class TestCreateUserRequest:
    async def test_create_user_request_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        service: Service = ServiceFactory()
        request_status = await status_service.read(
            session=db_session, data={"status_id": 3}
        )
        comment = faker.pystr(max_chars=255)
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_user_request",
                university_id=university.university_id,
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "service_id": service.service_id,
                "comment": comment,
            },
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f'Created user request with id {data.get("user_request_id")}',
            code=status.HTTP_200_OK,
        )
        assert data.get("comment") == comment
        assert data.get("user_id") == user.user_id
        assert data.get("service_id") == service.service_id
        assert data.get("faculty_id") == faculty.faculty_id
        assert data.get("university_id") == university.university_id
        assert data.get("status_id") == request_status.status_id

    async def test_create_user_request_422(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        comment = faker.pystr(max_chars=255)
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_user_request",
                university_id=university.university_id,
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "service_id": faker.pystr(max_chars=4),
                "comment": comment,
            },
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422
        )


class TestReadUserRequestBookingHostel:
    async def test_read_user_request_booking_hostel_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_booking_hostel",
                university_id=university.university_id,
            ),
            headers={"Authorization": f"Bearer {token}"}
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got user request booking hostel",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("full_name") == {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "middle_name": student.middle_name,
        }
        assert data.get("user_id") == user.user_id
        assert data.get("faculty_name") == faculty.name
        assert data.get("university_id") == university.university_id
        assert data.get("short_university_name") == university.short_university_name
        assert data.get("rector_full_name") == {
            "first_name": university.rector.first_name,
            "last_name": university.rector.last_name,
            "middle_name": university.rector.middle_name,
        }
        assert data.get("date_today") == datetime.date.today().strftime('%Y-%m-%d')
        assert data.get("start_year") == (
            datetime.date.today().year if datetime.date.today().month > 5
            else datetime.date.today().year - 1
        )
        assert data.get("finish_year") == (
            datetime.date.today().year if datetime.date.today().month < 5
            else datetime.date.today().year + 1
        )
        assert data.get("speciality_code") == speciality.code
        assert data.get("course") == student.course.value
        assert data.get("educ_level") == 'B' if student.course in {1, 2, 3, 4} else 'M'
        assert data.get("gender") == student.gender

    async def test_read_user_request_booking_hostel_422(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_booking_hostel",
                university_id=faker.pyint(min_value=7000),
            ),
            headers={"Authorization": f"Bearer {token}"}
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestCancelRequest:
    async def test_cancel_request_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        service: Service = ServiceFactory()
        request_status = await status_service.read(
            session=db_session, data={"status_id": 3}
        )
        cancel_status = await status_service.read(
            session=db_session, data={"status_id": 4}
        )
        user_request: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id
        )
        response = await async_client.request(
            method="PUT",
            url=app_fixture.url_path_for(
                name="update_cancel_user_request",
                university_id=university.university_id,
                user_request_id=user_request.user_request_id,
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "status_id": cancel_status.status_id,
            }
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message=f"Canceled request with id {user_request.user_request_id}",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data.get("user_request_id") == user_request.user_request_id
        assert data.get("created_at") == (
                user_request.created_at.strftime('%Y-%m-%d')
                + 'T' + user_request.created_at.strftime('%H:%M:%S') + '+00:00'
            )
        assert data.get("comment") == user_request.comment
        assert data.get("user_id") == user_request.user_id
        assert data.get("service_id") == user_request.service_id
        assert data.get("faculty_id") == user_request.faculty_id
        assert data.get("university_id") == user_request.university_id
        assert data.get("status_id") == cancel_status.status_id

    async def test_cancel_request_422(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        response = await async_client.request(
            method="PUT",
            url=app_fixture.url_path_for(
                name="update_cancel_user_request",
                university_id=university.university_id,
                user_request_id=faker.pyint(min_value=5000),
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "status_id": 4,
            }
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestCreateUserRequestReview:
    @pytest.mark.freeze_time('2017-05-21')
    async def test_create_user_request_review_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
            student_creation: Tuple[
                str, University, User, Student, Faculty, Speciality
            ],
            db_session: AsyncSession,
    ) -> None:
        token, university, user, student, faculty, speciality = student_creation
        service: Service = ServiceFactory()
        request_status = await status_service.read(
            session=db_session, data={"status_id": 3}
        )
        approve_status = await status_service.read(
            session=db_session, data={"status_id": 1}
        )
        user_request: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id
        )
        hostel: Hostel = HostelFactory(university_id=university.university_id)
        bed_place: BedPlace = BedPlaceFactory()
        room_number = faker.pyint()
        start_accommodation_date = faker.date_object().isoformat()
        end_accommodation_date = faker.date_object().isoformat()
        total_sum = faker.pyfloat(left_digits=5, right_digits=2, positive=True)
        payment_deadline_date = faker.date_object().isoformat()
        remark = faker.pystr(max_chars=255)
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_user_request_review",
                university_id=university.university_id,
                user_request_id=user_request.user_request_id,
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "status_id": approve_status.status_id,
                "room_number": room_number,
                "start_accommodation_date": start_accommodation_date,
                "end_accommodation_date": end_accommodation_date,
                "total_sum": total_sum,
                "payment_deadline_date": payment_deadline_date,
                "remark": remark,
                "hostel_id": hostel.hostel_id,
                "bed_place_id": bed_place.bed_place_id,
            },
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Created user request review",
            code=status.HTTP_200_OK,
        )
        assert data.get("created_at") == '2017-05-21T00:00:00+00:00'
        assert data.get("room_number") == room_number
        assert data.get("start_accommodation_date") == start_accommodation_date
        assert data.get("end_accommodation_date") == end_accommodation_date
        assert data.get("total_sum") == total_sum
        assert data.get("payment_deadline_date") == payment_deadline_date
        assert data.get("remark") == remark
        assert data.get("bed_place_id") == bed_place.bed_place_id
        assert data.get("reviewer") == user.user_id
        assert data.get("hostel_id") == hostel.hostel_id
        assert data.get("university_id") == university.university_id
        assert data.get("user_request_id") == user_request.user_request_id
