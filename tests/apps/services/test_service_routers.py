from pathlib import Path
from typing import Tuple, List
import datetime
import pytest
from collections import namedtuple
from faker import Faker
from fastapi import FastAPI, status, UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import json
import io

import settings
from apps.common.schemas import JSENDStatus
from apps.educational_institutions.models import Faculty, University, Speciality, Course
from apps.educational_institutions.services import faculty_service
from apps.hostel.models import Hostel, BedPlace
from apps.services.models import Service, UserRequest, UserRequestReview, Requisites, ServiceDocument
from apps.services.schemas import UserRequestReviewIn
from apps.services.services import user_document_service
from apps.services.utils import get_worksheet_cell_col_row
from apps.users.models import Student, User, UserFaculty
from tests.apps.conftest import assert_jsend_response, find_created_instance, status_service, speciality_service
from tests.apps.educational_institution.factories import CourseFactory, FacultyFactory, SpecialityFactory
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory
from tests.apps.services.factories import ServiceFactory, UserRequestFactory, StatusFactory, UserRequestReviewFactory, \
    RequisitesFactory, ServiceDocumentFactory
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

    async def test_create_user_request_review_422(
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
        bed_place: BedPlace = BedPlaceFactory()
        hostel: Hostel = HostelFactory(university_id=university.university_id)
        user_request: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=request_status.status_id
        )
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_user_request_review",
                university_id=university.university_id,  # TODO Integrity Error during none existed input
                user_request_id=user_request.user_request_id,  # TODO Integrity Error during none existed input
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "status_id": approve_status.status_id,
                "room_number": faker.pystr(),
                "start_accommodation_date": None,
                "end_accommodation_date": None,
                "total_sum": 0,
                "payment_deadline_date": None,
                "remark": None,
                "hostel_id": hostel.hostel_id,  # TODO Integrity Error during none existed input
                "bed_place_id": bed_place.bed_place_id,  # TODO Integrity Error during none existed input
            },
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestReadHostelAccommodation:
    async def test_read_hostel_accommodation_200(
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
        service_document: ServiceDocument = ServiceDocumentFactory(
            service_id=service.service_id, university_id=university.university_id
        )
        requisites: Requisites = RequisitesFactory(
            service_id=service.service_id, university_id=university.university_id
        )
        approve_status = await status_service.read(
            session=db_session, data={"status_id": 1}
        )
        hostel: Hostel = HostelFactory(university_id=university.university_id)
        bed_place: BedPlace = BedPlaceFactory()
        user_request: UserRequest = UserRequestFactory(
            user_id=user.user_id,
            service_id=service.service_id,
            faculty_id=faculty.faculty_id,
            university_id=university.university_id,
            status_id=approve_status.status_id
        )
        user_request_review: UserRequestReview = UserRequestReviewFactory(
            bed_place_id=bed_place.bed_place_id,
            reviewer=user.user_id,
            hostel_id=hostel.hostel_id,
            university_id=university.university_id,
            user_request_id=user_request.user_request_id,
        )
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_hostel_accommodation",
                university_id=university.university_id,
                user_request_id=user_request.user_request_id,
            ),
            headers={"Authorization": f"Bearer {token}"}
        )
        data = response.json()["data"]
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got hostel accommodation",
            code=status.HTTP_200_OK,
        )
        assert data.get("university_id") == user_request_review.university_id
        assert data.get(
            "user_request_review_id"
        ) == user_request_review.user_request_review_id
        assert data.get("hostel_name") == {
            "name": user_request_review.hostel.name,
            "number": user_request_review.hostel.number,
        }
        assert data.get("hostel_address") == {
            "city": user_request_review.hostel.city,
            "street": user_request_review.hostel.street,
            "build": user_request_review.hostel.build,
        }
        assert data.get("bed_place_name") == user_request_review.bed_place.bed_place_name
        assert data.get("month_price") == float(user_request_review.hostel.month_price)
        assert data.get(
            "start_accommodation_date"
        ) == user_request_review.start_accommodation_date
        assert data.get(
            "end_accommodation_date"
        ) == user_request_review.end_accommodation_date
        assert data.get("total_sum") == float(user_request_review.total_sum)
        assert data.get(
            "iban"
        ) == requisites.iban
        assert data.get("university_name") == university.university_name
        assert data.get(
            "organisation_code"
        ) == requisites.organisation_code
        assert data.get(
            "payment_recognition"
        ) == requisites.payment_recognition
        assert data.get("commandant_full_name") == {
            "first_name": user_request_review.hostel.commandant.first_name,
            "last_name": user_request_review.hostel.commandant.last_name,
            "middle_name": user_request_review.hostel.commandant.middle_name,
        }
        assert data.get(
            "telephone_number"
        ) == user_request_review.hostel.commandant.telephone_number
        assert data.get(
            "documents"
        ) == service_document.documents

    async def test_read_hostel_accommodation_200_empty(
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
                name="read_hostel_accommodation",
                university_id=faker.pyint(min_value=3000),
                user_request_id=faker.pyint(min_value=2500),
            ),
            headers={"Authorization": f"Bearer {token}"}
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got hostel accommodation",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        assert data is None


class TestReadUserDocumentList:
    async def test_read_user_document_list_200(
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
        user_documents = []
        for _ in range(3):
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
                    "comment": faker.pystr(max_chars=255),
                },
            )
            data = response.json()["data"]
            user_request_id = data.get("user_request_id")
            user_documents.append(
                await user_document_service.read(
                    session=db_session, data={"user_request_id": user_request_id}
                )
            )

        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_documents_list",
                university_id=university.university_id
            ),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got user documents list",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        for user_document in user_documents:
            created_instance = find_created_instance(
                user_document.user_document_id, data, "user_document_id"
            )
            assert created_instance.get("university_id") == university.university_id
            assert created_instance.get("user_document_id") == user_document.user_document_id
            assert created_instance.get("name") == user_document.name
            assert created_instance.get("created_at") == (
                    user_document.created_at.strftime('%Y-%m-%d')
                    + 'T' + user_document.created_at.strftime('%H:%M:%S.%f') + '+00:00'
            )
            assert created_instance.get("updated_at") == (
                    user_document.updated_at.strftime('%Y-%m-%d')
                    + 'T' + user_document.updated_at.strftime('%H:%M:%S.%f') + '+00:00'
            )


class TestReadUserRequestDetails:
    async def test_read_user_request_details_200_full(
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
        hostel: Hostel = HostelFactory(university_id=university.university_id)
        bed_place: BedPlace = BedPlaceFactory()
        approved_status = await status_service.read(
            session=db_session, data={"status_id": 1}
        )
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
                "comment": faker.pystr(max_chars=254),
            },
        )
        user_request_out = response.json()["data"]
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(
                name="create_user_request_review",
                university_id=university.university_id,
                user_request_id=user_request_out.get("user_request_id")
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            json={
                "status_id": approved_status.status_id,
                "room_number": faker.pyint(),
                "start_accommodation_date": faker.date(),
                "end_accommodation_data": faker.date(),
                "total_sum": float(faker.pydecimal(
                    left_digits=5, right_digits=2, positive=True
                )),
                "payment_deadline_date": faker.date(),
                "hostel_id": hostel.hostel_id,
                "bed_place_id": bed_place.bed_place_id,
            },
        )
        user_request_review_out = response.json()["data"]
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_details",
                university_id=university.university_id,
                user_request_id=user_request_out.get("user_request_id"),
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got request details",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        user_documents = await user_document_service.list(
            session=db_session,
            filters={"user_request_id": user_request_out.get("user_request_id")},
        )
        assert data.get("user_request_id") == user_request_out.get("user_request_id")
        assert data.get("university_id") == university.university_id
        assert data.get("created_at") == user_request_out.get("created_at")
        assert data.get("service_name") == service.service_name
        assert data.get("status_name") == approved_status.status_name
        assert data.get("status_id") == approved_status.status_id
        assert data.get("comment") == user_request_out.get("comment")
        assert data.get("hostel_name") == {
            "name": hostel.name, "number": hostel.number
        }
        assert data.get("room_number") == user_request_review_out.get("room_number")
        assert data.get("bed_place_name") == bed_place.bed_place_name
        assert data.get("remark") == user_request_review_out.get("remark")
        assert data.get("documents") == [{
            "id": user_document.user_document_id,
            "name": user_document.name,
            "created_at": (user_document.created_at.strftime('%Y-%m-%d')
                           + 'T' + user_document.created_at.strftime('%H:%M:%S.%f')
                           + '+00:00'
                           )
        } for user_document in user_documents]

    async def test_read_user_request_details_200_empty(
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
                "comment": faker.pystr(max_chars=254),
            },
        )
        user_request_out = response.json()["data"]
        response = await async_client.get(
            url=app_fixture.url_path_for(
                name="read_user_request_details",
                university_id=university.university_id,
                user_request_id=user_request_out.get("user_request_id"),
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got request details",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        user_documents = await user_document_service.list(
            session=db_session,
            filters={"user_request_id": user_request_out.get("user_request_id")},
        )
        assert data.get("user_request_id") == user_request_out.get("user_request_id")
        assert data.get("university_id") == university.university_id
        assert data.get("created_at") == user_request_out.get("created_at")
        assert data.get("service_name") == service.service_name
        assert data.get("status_name") == request_status.status_name
        assert data.get("status_id") == request_status.status_id
        assert data.get("comment") == user_request_out.get("comment")
        assert data.get("hostel_name") == {
            "name": None, "number": None
        }
        assert data.get("room_number") is None
        assert data.get("bed_place_name") is None
        assert data.get("remark") is None
        assert data.get("documents") == [{
            "id": user_document.user_document_id,
            "name": user_document.name,
            "created_at": (user_document.created_at.strftime('%Y-%m-%d')
                           + 'T' + user_document.created_at.strftime('%H:%M:%S.%f')
                           + '+00:00'
                           )
        } for user_document in user_documents]

    async def test_read_user_request_details_422(
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
                name="read_user_request_details",
                university_id=university.university_id,
                user_request_id=faker.pyint(min_value=2900),
            ),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )
        assert_jsend_response(
            response=response,
            http_code=422,
            status=JSENDStatus.FAIL,
            message="Validation error.",
            code=422,
        )


class TestCreateStudentsListFromFile:
    async def test_create_students_list_from_file_200(
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
        courses: Course = CourseFactory.create_batch(size=10)
        file_path = Path(settings.BASE_DIR / "tests" / "samples" / "Form.xlsx").as_posix()
        with io.open(file_path, 'rb', buffering=0) as f:
            data = f.read()
        upload_file = UploadFile(
            filename="Form.xlsx",
            file=io.BytesIO(data)
        )
        StudentData = namedtuple('StudentData', [
            'last_name',
            'first_name',
            'middle_name',
            'telephone',
            'course',
            'speciality_id',
            'faculty_id',
            'gender',
        ])
        student_data_list = []
        worksheet, cell, col, row = get_worksheet_cell_col_row(upload_file)
        for i in range(row, len(worksheet.col(1))):
            faculty_list = await faculty_service.list(
                session=db_session, filters={"shortname": cell(i, col + 7)}
            )
            if not faculty_list:
                faculty: Faculty = FacultyFactory(
                    university_id=university.university_id,
                    shortname=cell(i, col + 7)
                )
            faculty_id = (
                faculty_list[0].faculty_id if faculty_list else faculty.faculty_id
            )
            speciality_list = await speciality_service.list(
                session=db_session,
                filters={
                    "faculty_id": faculty_id,
                    "name": cell(i, col + 6),
                }
            )
            if not speciality_list:
                speciality: Speciality = SpecialityFactory(
                    faculty_id=faculty_id, name=cell(i, col + 6)
                )
            speciality_id = (
                speciality_list[0].speciality_id if speciality_list
                else speciality.speciality_id
            )
            student_data_list.append(
                StudentData(
                    cell(i, col),
                    cell(i, col + 1),
                    cell(i, col + 2),
                    cell(i, col + 3),
                    cell(i, col + 4),
                    speciality_id,
                    faculty_id,
                    cell(i, col + 8)
                )
            )
        response = await async_client.post(
            url=app_fixture.url_path_for(
                name="create_students_list_from_file",
                university_id=university.university_id,
            ),
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={"file": open(file_path, 'rb')},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Created students list from file",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        for student in student_data_list:
            created_instance = find_created_instance(
                student.telephone, data, "telephone_number"
            )
            assert created_instance.get("first_name") == student.first_name
            assert created_instance.get("last_name") == student.last_name
            assert created_instance.get("middle_name") == student.middle_name
            assert created_instance.get("telephone_number") == student.telephone
            assert created_instance.get("gender") == student.gender
            assert created_instance.get("course_id") == student.course
            assert created_instance.get("speciality_id") == student.speciality_id
            assert created_instance.get("user_id") is None
            assert created_instance.get("faculty_id") == student.faculty_id


