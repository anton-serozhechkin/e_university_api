from models.user_faculty import user_faculty as user_faculty_table
from models.user_request import user_request as user_request_table
from models.user_request_review import user_request_review as user_request_rev_table
from models.user_document import create_user_document
from models.user_request_exist_view import user_request_exist_view
from models.user_request_booking_hostel_view import user_request_booking_hostel_view
from models.user_request_list_view import user_request_list_view
from models.hostel_accommodation_view import hostel_accommodation_view
from models.user_request_details_view import user_request_details_view
from models.status import STATUS_MAPPING
from schemas.user_request import (CreateUserRequestIn, CreateUserRequestOut,
                                  UserRequestExistenceOut, UserRequestBookingHostelOut, UserRequestReviewIn,
                                  UserRequestReviewOut,
                                  UserRequestsListOut, CancelRequestIn, CancelRequestOut, HostelAccomodationViewOut,
                                  UserRequestDetailsViewOut)
from handlers.current_user import get_current_user
from db import database

from datetime import datetime
from typing import List
import json

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/{university_id}/user-request-existence/{service_id}/",
            response_model=JSENDOutSchema[UserRequestExistenceOut], tags=["Student dashboard"])
async def check_user_request_existence(university_id: int, service_id: int, user=Depends(get_current_user)):
    query = user_request_exist_view.select().where(user_request_exist_view.c.user_id == user.user_id,
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
    return JSENDOutSchema[UserRequestExistenceOut](
        data=response,
        message="Get user request existence"
    )


@router.get("/{university_id}/user-request/", response_model=JSENDOutSchema[List[UserRequestsListOut]],
            tags=["Student dashboard"])
async def read_user_request_list(university_id: int, user=Depends(get_current_user)):
    query = user_request_list_view.select().where(user_request_list_view.c.user_id == user.user_id,
                                                  user_request_list_view.c.university_id == university_id)
    return JSENDOutSchema[List[UserRequestsListOut]](
        data=await database.fetch_all(query),
        message="Get user requests list"
    )


@router.post("/{university_id}/user-request/", response_model=JSENDOutSchema[CreateUserRequestOut],
             tags=["Student dashboard"])
async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user=Depends(get_current_user)):
    query = user_faculty_table.select().where(user_faculty_table.c.user_id == user.user_id)
    user_faculty_result = await database.fetch_one(query)
    query = user_request_table.insert().values(user_id=user.user_id,
                                               service_id=user_request.service_id,
                                               date_created=datetime.now(),
                                               comment=user_request.comment,
                                               faculty_id=user_faculty_result.faculty_id,
                                               university_id=university_id,
                                               status_id=STATUS_MAPPING.get("Розглядається"))

    last_record_id = await database.execute(query)

    query = user_request_booking_hostel_view.select().where(user_request_booking_hostel_view.c.user_id == user.user_id,
                                                            user_request_booking_hostel_view.c.university_id == university_id)
    result = await database.fetch_one(query)

    prepared_data = {
        "context": result,
        "service_id": user_request.service_id,
        "user_request_id": last_record_id
    }

    await create_user_document(**prepared_data)

    return JSENDOutSchema[CreateUserRequestOut](
        data={
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": last_record_id
        },
        message=f"Created user request with id {last_record_id}"
    )


@router.get("/{university_id}/user-request-booking-hostel/", response_model=JSENDOutSchema[UserRequestBookingHostelOut],
            tags=["Student dashboard"])
async def read_user_request_booking_hostel(university_id: int, user=Depends(get_current_user)):
    query = user_request_booking_hostel_view.select().where(user_request_booking_hostel_view.c.user_id == user.user_id,
                                                            user_request_booking_hostel_view.c.university_id == university_id)
    return JSENDOutSchema[UserRequestBookingHostelOut](
        data=await database.fetch_one(query),
        message="Get user request booking hostel"
    )


@router.put("/{university_id}/user-request/{user_request_id}", response_model=JSENDOutSchema[CancelRequestOut],
            tags=["Student dashboard"])
async def cancel_request(university_id: int, user_request_id: int, cancel_request: CancelRequestIn,
                         user=Depends(get_current_user)):
    CancelRequestIn(status_id=cancel_request.status_id)
    query = user_request_table.update().where(user_request_table.c.user_request_id == user_request_id).values(
        status_id=cancel_request.status_id)
    await database.execute(query)

    return JSENDOutSchema[CancelRequestOut](
        data={
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        },
        message=f"Canceled request with id {user_request_id}"
    )


@router.post("/{university_id}/user-request-review/{user_request_id}/",
             response_model=JSENDOutSchema[UserRequestReviewOut],
             tags=["Admin dashboard"])
async def create_user_request_review(university_id: int, user_request_id: int, user_request_review: UserRequestReviewIn,
                                     user=Depends(get_current_user)):
    query = user_request_rev_table.insert().values(university_id=university_id,
                                                   user_request_id=user_request_id,
                                                   date_created=datetime.now(),
                                                   reviewer=user.user_id,
                                                   hostel_id=user_request_review.hostel_id,
                                                   room_number=user_request_review.room_number,
                                                   start_date_accommodation=user_request_review.start_date_accommodation,
                                                   end_date_accommodation=user_request_review.end_date_accommodation,
                                                   total_sum=user_request_review.total_sum,
                                                   payment_deadline=user_request_review.payment_deadline,
                                                   remark=user_request_review.remark,
                                                   date_review=datetime.now(),
                                                   bed_place_id=user_request_review.bed_place_id)

    last_record_id = await database.execute(query)

    query = user_request_table.update().values(status_id=user_request_review.status_id).where(
        user_request_table.c.user_request_id == user_request_id)
    await database.execute(query)

    return JSENDOutSchema[UserRequestReviewOut](
        data={
            "status_id": user_request_review.status_id,
            "user_request_review_id": last_record_id
        },
        message="Created user request review"
    )


@router.get("/{university_id}/hostel-accommodation/{user_request_id}",
            response_model=JSENDOutSchema[HostelAccomodationViewOut], tags=["Student dashboard"])
async def read_hostel_accommodation(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    query = hostel_accommodation_view.select().where(hostel_accommodation_view.c.university_id == university_id,
                                                     hostel_accommodation_view.c.user_request_id == user_request_id)
    response = await database.fetch_one(query)

    response.documents = json.loads(response.documents)     # TODO AttributeError: 'NoneType' object has no attribute 'documents'

    response.hostel_name = json.loads(response.hostel_name)
    response.hostel_address = json.loads(response.hostel_address)
    return JSENDOutSchema[HostelAccomodationViewOut](
        data=response,
        message="Get hostel accommodation"
    )


@router.get("/{university_id}/user-request/{user_request_id}", response_model=JSENDOutSchema[UserRequestDetailsViewOut],
            tags=["Student dashboard"])
async def read_request_details(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    query = user_request_details_view.select().where(user_request_details_view.c.university_id == university_id,
                                                     user_request_details_view.c.user_request_id == user_request_id)

    response = await database.fetch_one(query)

    response.documents = json.loads(response.documents)
    response.hostel_name = json.loads(response.hostel_name)
    return JSENDOutSchema[UserRequestDetailsViewOut](
        data=response,
        message="Get request details"
    )
