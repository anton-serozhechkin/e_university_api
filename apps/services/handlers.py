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


@services_router.get("/{university_id}/user-request-existence/{service_id}/",
                     name="read_user_request_existence",
                     response_model=JSENDOutSchema[UserRequestExistenceOut],
                     summary="Check user request existence",
                     responses={
                         200: {"description": "Successful get response with info about existence user request response"}
                     },
                     tags=["Student dashboard"]
                     )
async def check_user_request_existence(university_id: int, service_id: int, user=Depends(get_current_user)):
    """
    **Checking user request existence**

    **Path**
    - **university_id**: user university id
    - **service_id**: checking service id

    **Return**: user request id; user request status; user request existence
    """
    query = select(user_request_exist_view).where(user_request_exist_view.c.user_id == user.user_id,
                                                  user_request_exist_view.c.university_id == university_id,
                                                  user_request_exist_view.c.service_id == service_id)
    user_request_result = await database.fetch_one(query)
    if user_request_result:
        response = {
            "user_request_id": user_request_result.user_request_id,
            "status": json.loads(user_request_result.status),
            "user_request_exist": True
        }
    else:
        response = {
            "user_request_id": None,
            "status": None,
            "user_request_exist": False
        }
    return {
        "data": response,
        "message": "Got user request existence"
    }


@services_router.get("/{university_id}/user-request/",
                     name="read_user_request_list",
                     response_model=JSENDOutSchema[List[UserRequestsListOut]],
                     summary="Get user request list",
                     responses={200: {"description": "Successful get university user request list response"}},
                     tags=["Student dashboard"]
                     )
async def read_user_request_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_request_list_view).where(user_request_list_view.c.user_id == user.user_id,
                                                 user_request_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": "Got user requests list"
    }


@services_router.post("/{university_id}/user-request/",
                      name="create_user_request",
                      response_model=JSENDOutSchema[CreateUserRequestOut],
                      summary="Create user request",
                      responses={200: {"description": "Successful create user request response"}},
                      tags=["Student dashboard"])
async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user=Depends(get_current_user)):
    """
    **Create user request**

    **Path**:
    - **university_id**: user university id

    **Input**:
    - **service_id**: service id in database, required
    - **comment*: comment for the creating user request

    **Return**: user request id; request status id
    """
    query = select(UserFaculty).where(UserFaculty.user_id == user.user_id)
    user_faculty_result = await database.fetch_one(query)
    query = insert(UserRequest).values(date_created=datetime.now(),
                                       comment=user_request.comment,
                                       user_id=user.user_id,
                                       service_id=user_request.service_id,
                                       faculty_id=user_faculty_result.faculty_id,
                                       university_id=university_id,
                                       status_id=STATUS_MAPPING.get("Розглядається"))

    last_record_id = await database.execute(query)

    query = select(user_request_booking_hostel_view).where(user_request_booking_hostel_view.c.user_id == user.user_id,
                                                           user_request_booking_hostel_view.c.university_id == university_id)

    result = await database.fetch_one(query)

    prepared_data = {
        "context": result,
        "service_id": user_request.service_id,
        "user_request_id": last_record_id
    }

    await create_user_document(**prepared_data)

    return {
        "data": {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": last_record_id
        },
        "message": f"Created user request with id {last_record_id}",
        "code": http_status.HTTP_201_CREATED
    }


@services_router.get("/{university_id}/user-request-booking-hostel/",
                     name="read_user_request_booking_hostel",
                     response_model=JSENDOutSchema[UserRequestBookingHostelOut],
                     summary="Get user request booking hostel",
                     responses={200: {"description": "Successful get user request booking hostel response"}},
                     tags=["Student dashboard"])
async def read_user_request_booking_hostel(university_id: int, user=Depends(get_current_user)):
    query = select(user_request_booking_hostel_view).where(user_request_booking_hostel_view.c.user_id == user.user_id,
                                                           user_request_booking_hostel_view.c.university_id == university_id)
    return {
        "data": await database.fetch_one(query),
        "message": "Got user request booking hostel"
    }


@services_router.put("/{university_id}/user-request/{user_request_id}",
                     name="update_cancel_user_request",
                     response_model=JSENDOutSchema[CancelRequestOut],
                     summary="Cancel user request",
                     responses={200: {"description": "Successful cancel user request response"}},
                     tags=["Student dashboard"])
async def cancel_request(university_id: int, user_request_id: int, cancel_request: CancelRequestIn,
                         user=Depends(get_current_user)):
    """
    **Cancel user request**

    **Path**:
    - **university_id**: user university id
    - **user_request_id**: user request id

    **Input**:
    - **status_id**: user request status id, required

    **Return**: canceled user request id and status id
    """
    CancelRequestIn(status_id=cancel_request.status_id)
    query = update(UserRequest).where(UserRequest.user_request_id == user_request_id).values(
        status_id=cancel_request.status_id)
    await database.execute(query)

    return {
        "data": {
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        },
        "message": f"Canceled request with id {user_request_id}",
        "code": http_status.HTTP_200_OK
    }


@services_router.post("/{university_id}/user-request-review/{user_request_id}/",
                      name="create_user_request_review",
                      response_model=JSENDOutSchema[UserRequestReviewOut],
                      summary="Create user request review",
                      responses={200: {"description": "Successful create user request review response"}},
                      tags=["Admin dashboard"])
async def create_user_request_review(university_id: int, user_request_id: int, user_request_review: UserRequestReviewIn,
                                     user=Depends(get_current_user)):
    """
    **Create user request review**

    **Path**:
    - **university_id**: user university id
    - **user_request_id**: user request id

    **Input**:
    - **status_id**: user request status id, required
    - **room_number**: user room number, required
    - **start_date_accommodation**: starting datetime hostel accommodation, required
    - **end_date_accommodation**: end datetime hostel accommodation, required
    - **total_sum**: total sum of hostel accommodation payment, required
    - **payment_deadline**: deadline datetime for hostel accommodation payment, required
    - **remark**: additional info for request review, required
    - **hostel_id**: hostel id in the database, required
    - **bed_place_id**: hostel bed place id, required

    **Return**: user request status id; user request review id
    """
    query = insert(UserRequestReview).values(university_id=university_id,
                                             user_request_id=user_request_id,
                                             date_created=datetime.now(),
                                             reviewer=user.user_id,
                                             hostel_id=user_request_review.hostel_id,
                                             room_number=user_request_review.room_number,
                                             start_date_accommodation=user_request_review.start_date_accommodation.now(),
                                             end_date_accommodation=user_request_review.end_date_accommodation.now(),
                                             total_sum=user_request_review.total_sum,
                                             payment_deadline=user_request_review.payment_deadline.now(),
                                             remark=user_request_review.remark,
                                             date_review=datetime.now(),
                                             bed_place_id=user_request_review.bed_place_id)

    last_record_id = await database.execute(query)

    query = update(UserRequest).values(status_id=user_request_review.status_id).where(UserRequest.user_request_id == user_request_id)
    await database.execute(query)

    return {
        "data": {
            "status_id": user_request_review.status_id,
            "user_request_review_id": last_record_id
        },
        "message": "Created user request review",
        "code": http_status.HTTP_201_CREATED
    }


@services_router.get("/{university_id}/hostel-accommodation/{user_request_id}",
                     name="read_hostel_accommodation",
                     response_model=JSENDOutSchema[HostelAccomodationViewOut],
                     summary="Get hostel accommodation",
                     responses={200: {"description": "Successful get user request hostel accommodation response"}},
                     tags=["Student dashboard"])
async def read_hostel_accommodation(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    query = select(hostel_accommodation_view).where(hostel_accommodation_view.c.university_id == university_id,
                                                    hostel_accommodation_view.c.user_request_id == user_request_id)
    response = await database.fetch_one(query)

    response.documents = json.loads(response.documents)  # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's heppend only if user request doesn't have review)

    response.hostel_name = json.loads(response.hostel_name)
    response.hostel_address = json.loads(response.hostel_address)
    return {
        "data": response,
        "message": "Got hostel accommodation"
    }


@services_router.get("/{university_id}/user-request/{user_request_id}",
                     name="read_user_request_details",
                     response_model=JSENDOutSchema[UserRequestDetailsViewOut],
                     summary="Get user request",
                     responses={200: {"description": "Successful get user request response"}},
                     tags=["Student dashboard"])
async def read_request_details(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    query = select(user_request_details_view).where(user_request_details_view.c.university_id == university_id,
                                                    user_request_details_view.c.user_request_id == user_request_id)

    response = await database.fetch_one(query)

    response.documents = json.loads(response.documents)
    response.hostel_name = json.loads(response.hostel_name)
    return {
        "data": response,
        "message": "Got request details"
    }


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



