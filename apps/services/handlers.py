from apps.common.exceptions import BackendException
from apps.services.models import STATUS_MAPPING
from apps.services.schemas import CancelRequestIn, CreateUserRequestIn, UserRequestReviewIn
from apps.services.services import (
    create_user_document, hostel_accommodation_service, request_existence_service, user_request_list_service,
    user_faculty_service, user_request_service, user_request_booking_hostel_service, user_request_review_service,
    user_request_detail_service
)
from apps.users.schemas import UserOut
from apps.common.db import database
from apps.common.exceptions import BackendException
from apps.educational_institutions.models import Faculty, Speciality
from apps.services.models import user_request_exist_view, user_request_list_view, STATUS_MAPPING, UserRequest, \
    user_request_booking_hostel_view, UserRequestReview, hostel_accommodation_view, user_request_details_view
from apps.services.schemas import UserRequestExistenceOut, UserRequestsListOut, CreateUserRequestOut, \
    CreateUserRequestIn, UserRequestBookingHostelOut, CancelRequestOut, CancelRequestIn, UserRequestReviewOut, \
    UserRequestReviewIn, HostelAccomodationViewOut, UserRequestDetailsViewOut
from apps.services.services import create_user_document
from apps.users.handlers import get_current_user
from apps.users.models import UserFaculty
from apps.users.schemas import CreateStudentIn, StudentsListOut

from datetime import datetime
from typing import List
import json
import xlrd
from collections import defaultdict
from fastapi import Depends, APIRouter, File, status as http_status, UploadFile
from sqlalchemy import select, insert, update
from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema
services_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceHandler:

    async def read_user_request_existence(
            self,
            *,
            request: Request,
            university_id: int,
            service_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        user_request_result = await request_existence_service.read(
            session=session,
            data={"university_id": university_id, "service_id": service_id, "user_id": user.user_id}
        )
        if user_request_result:
            return {
                "user_request_id": user_request_result.user_request_id,
                "status": user_request_result.status,
                "user_request_exist": True
            }
        return {
            "user_request_id": None,
            "status": None,
            "user_request_exist": False
        }

    async def read_user_request_list(
            self,
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        return await user_request_list_service.list(
            session=session,
            filters={"university_id": university_id, "user_id": user.user_id}
        )

    async def create_user_request(
            self,
            *,
            request: Request,
            university_id: int,
            user_request: CreateUserRequestIn,
            user: UserOut,
            session: AsyncSession
    ):
        user_faculty_result = await user_faculty_service.read(data={"user_id": user.user_id}, session=session)
        data = {"date_created": datetime.now(),
                "comment": user_request.comment,
                "user_id": user.user_id,
                "service_id": user_request.service_id,
                "faculty_id": user_faculty_result.faculty_id,
                "university_id": university_id,
                "status_id": STATUS_MAPPING.get("Розглядається")}
        user_request = await user_request_service.create(session=session, data=data)
        result = await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id})
        prepared_data = {
            "context": result,
            "service_id": user_request.service_id,
            "user_request_id": user_request.user_request_id
        }
        await create_user_document(**prepared_data)
        return {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": user_request.user_request_id
        }

    async def read_user_request_booking_hostel(
            self,
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        return await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id})

    async def cancel_request(
            self,
            *,
            request: Request,
            user_request_id: int,
            cancel_request: CancelRequestIn,
            session: AsyncSession):
        CancelRequestIn(status_id=cancel_request.status_id)
        await user_request_service.update(
                session=session,
                data={"user_request_id": user_request_id},
                obj=cancel_request)
        return {
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        }

    async def create_user_request_review(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            user_request_review: UserRequestReviewIn,
            user: UserOut,
            session: AsyncSession):
        created_user_request_review = await user_request_review_service.create(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id,
                "date_created": datetime.now(),
                "reviewer": user.user_id,
                "hostel_id": user_request_review.hostel_id,
                "room_number": user_request_review.room_number,
                "start_date_accommodation": user_request_review.start_date_accommodation.now(),
                "end_date_accommodation": user_request_review.end_date_accommodation.now(),
                "total_sum": user_request_review.total_sum,
                "payment_deadline": user_request_review.payment_deadline.now(),
                "remark": user_request_review.remark,
                "bed_place_id": user_request_review.bed_place_id
            })
        await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj={"status_id": user_request_review.status_id}
        )
        return {
            "status_id": user_request_review.status_id,
            "user_request_review_id": created_user_request_review.user_request_review_id
        }

    async def read_hostel_accommodation(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession):
        response = await hostel_accommodation_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })
        # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's heppend only if user request doesn't have review)
        return response

    async def read_request_details(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession):
        return await user_request_detail_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })


service_handler = ServiceHandler()


@services_router.post("/{university_id}/create_students/",
                      name="create_students_from_file",
                      response_model=JSENDOutSchema[StudentsListOut],
                      summary="Create students from file",
                      responses={200: {"description": "Successful create students from file response"}},
                      tags=['Admin dashboard'])
async def create_students_from_file(
        university_id: int,
        file: UploadFile = File(...),
        user=Depends(get_current_user)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise BackendException(
            message="Uploaded file have invalid type.",
            code=http_status.HTTP_406_NOT_ACCEPTABLE
        )
    query = select(Faculty, Speciality).filter(
        Speciality.faculty_id == Faculty.faculty_id
    ).where(Faculty.university_id == university_id)
    specialties, faculty_dict, schema_list = await database.fetch_all(query), defaultdict(dict), []
    for specialty in specialties:
        faculty_dict[specialty.shortname]["faculty_id"] = specialty.faculty_id
        faculty_dict[specialty.shortname][specialty.name_1] = specialty.speciality_id
    workbook = xlrd.open_workbook(file_contents=file.file.read())
    worksheet = workbook.sheet_by_name("список студентів")
    row, col = 0, 0
    for i, elem in enumerate(worksheet.col(1)):
        if elem.value:
            row = i + 1
            break
        if i > 100:
            raise BackendException(
                message="Empty second column. Please, check the correctness of the file content.",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
    for j, elem in enumerate(worksheet.row(row-1)):
        if elem.value == "Прізвище":
            col = j
            break
        if j > 100:
            raise BackendException(
                message="Can't find cell with content 'Прізвище'. Please, check the correctness of the file content.",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
    for i in range(row, len(worksheet.col(1))):
        if worksheet.cell_value(i, col + 7) not in faculty_dict:
            raise BackendException(
                message=f"Row {i}. There is no such faculty name.",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
        specialties_dict = faculty_dict.get(worksheet.cell_value(i, col + 7))
        if worksheet.cell_value(i, col + 6) not in specialties_dict:
            raise BackendException(
                message=f"Row {i}. There is no such speciality in {worksheet.cell_value(i, col + 7)} faculty",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
        schema = CreateStudentIn(
            full_name=worksheet.cell_value(i, col),
            telephone_number=worksheet.cell_value(i, col + 3),
            course_id=worksheet.cell_value(i, col + 4),
            faculty_id=specialties_dict.get("faculty_id"),
            speciality_id=specialties_dict.get(worksheet.cell_value(i, col + 6)),
            gender=worksheet.cell_value(i, col + 8)
        )
        schema_list.append(schema)

    print(schema_list, 888)



