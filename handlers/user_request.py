from sqlalchemy import select, update, insert

from models.user_faculty import UserFaculty
from models.user_request import UserRequest
from models.user_request_review import UserRequestReview
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

from fastapi import Depends, APIRouter, status as http_status

from schemas.jsend import JSENDOutSchema, JSENDErrorOutSchema

router = APIRouter(
    responses={422: {"model": JSENDErrorOutSchema, "description": "ValidationError"}}
)


@router.get("/{university_id}/user-request-existence/{service_id}/",
            name="check_user_request_existence",
            response_model=JSENDOutSchema[UserRequestExistenceOut],
            summary="Check user request existence",
            responses={200: {"description": "Successful get response with info about existence user request response"}},
            tags=["Student dashboard"])
async def check_user_request_existence(university_id: int, service_id: int, user=Depends(get_current_user)):
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


@router.get("/{university_id}/user-request/",
            name="get_user_request_list",
            response_model=JSENDOutSchema[List[UserRequestsListOut]],
            summary="Get user request list",
            responses={200: {"description": "Successful get university user request list response"}},
            tags=["Student dashboard"])
async def read_user_request_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_request_list_view).where(user_request_list_view.c.user_id == user.user_id,
                                                 user_request_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": "Got user requests list"
    }


@router.post("/{university_id}/user-request/",
             name="post_user_request",
             response_model=JSENDOutSchema[CreateUserRequestOut],
             summary="Create user request",
             responses={200: {"description": "Successful create user request response"}},
             tags=["Student dashboard"])
async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user=Depends(get_current_user)):
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


@router.get("/{university_id}/user-request-booking-hostel/",
            name="get_user_request_booking_hostel",
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


@router.put("/{university_id}/user-request/{user_request_id}",
            name="put_cancel_user_request",
            response_model=JSENDOutSchema[CancelRequestOut],
            summary="Cancel user request",
            responses={200: {"description": "Successful cancel user request response"}},
            tags=["Student dashboard"])
async def cancel_request(university_id: int, user_request_id: int, cancel_request: CancelRequestIn,
                         user=Depends(get_current_user)):
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
        "code": http_status.HTTP_202_ACCEPTED
    }


@router.post("/{university_id}/user-request-review/{user_request_id}/",
             name="post_user_request_review",
             response_model=JSENDOutSchema[UserRequestReviewOut],
             summary="Create user request review",
             responses={200: {"description": "Successful create user request review response"}},
             tags=["Admin dashboard"])
async def create_user_request_review(university_id: int, user_request_id: int, user_request_review: UserRequestReviewIn,
                                     user=Depends(get_current_user)):
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


@router.get("/{university_id}/hostel-accommodation/{user_request_id}",
            name="get_hostel_accommodation",
            response_model=JSENDOutSchema[HostelAccomodationViewOut],
            summary="Get hostel accommodation",
            responses={200: {"description": "Successful get user request hostel accommodation response"}},
            tags=["Student dashboard"])
async def read_hostel_accommodation(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    query = select(hostel_accommodation_view).where(hostel_accommodation_view.c.university_id == university_id,
                                                    hostel_accommodation_view.c.user_request_id == user_request_id)
    response = await database.fetch_one(query)

    response.documents = json.loads(response.documents)     # TODO AttributeError: 'NoneType' object has no attribute 'documents'

    response.hostel_name = json.loads(response.hostel_name)
    response.hostel_address = json.loads(response.hostel_address)
    return {
        "data": response,
        "message": "Got hostel accommodation"
    }


@router.get("/{university_id}/user-request/{user_request_id}",
            name="get_request_details",
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
