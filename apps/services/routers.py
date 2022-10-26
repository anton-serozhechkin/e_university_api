from apps.services.schemas import UserRequestExistenceOut, UserRequestsListOut, CreateUserRequestOut, \
    CreateUserRequestIn, UserRequestBookingHostelOut, CancelRequestOut, CancelRequestIn, UserRequestReviewOut, \
    UserRequestReviewIn, HostelAccomodationViewOut, UserRequestDetailsViewOut
from apps.users.handlers import get_current_user
from apps.services import handlers

from typing import List

from fastapi import Depends, APIRouter
from apps.common.schemas import JSENDOutSchema

services_router = APIRouter()


@services_router.get("/{university_id}/user-request-existence/{service_id}/",
            response_model=JSENDOutSchema[UserRequestExistenceOut], tags=["Student dashboard"])
async def check_user_request_existence(university_id: int, service_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_user_request_existence(university_id, service_id, user),
        "message": "Got user request existence"
    }


@services_router.get("/{university_id}/user-request/", response_model=JSENDOutSchema[List[UserRequestsListOut]],
                     tags=["Student dashboard"])
async def read_user_request_list(university_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_user_request_list(university_id, user),
        "message": "Got user requests list"
    }


@services_router.post("/{university_id}/user-request/", response_model=JSENDOutSchema[CreateUserRequestOut],
                      tags=["Student dashboard"])
async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user=Depends(get_current_user)):
    response = handlers.create_user_request(university_id, user_request, user)
    return {
        "data": response,
        "message": f"Created user request with id {response['user_request_id']}"
    }


@services_router.get("/{university_id}/user-request-booking-hostel/", response_model=JSENDOutSchema[UserRequestBookingHostelOut],
                     tags=["Student dashboard"])
async def read_user_request_booking_hostel(university_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_user_request_booking_hostel(university_id, user),
        "message": "Got user request booking hostel"
    }


@services_router.put("/{university_id}/user-request/{user_request_id}", response_model=JSENDOutSchema[CancelRequestOut],
                     tags=["Student dashboard"])
async def cancel_request(university_id: int, user_request_id: int, cancel_request: CancelRequestIn,
                         user=Depends(get_current_user)):
    return {
        "data": handlers.cancel_request(user_request_id, cancel_request),
        "message": f"Canceled request with id {user_request_id}"
    }


@services_router.post("/{university_id}/user-request-review/{user_request_id}/",
                      response_model=JSENDOutSchema[UserRequestReviewOut],
                      tags=["Admin dashboard"])
async def create_user_request_review(university_id: int, user_request_id: int, user_request_review: UserRequestReviewIn,
                                     user=Depends(get_current_user)):
    return {
        "data": handlers.create_user_request_review(university_id, user_request_id, user_request_review, user),
        "message": "Created user request review"
    }


@services_router.get("/{university_id}/hostel-accommodation/{user_request_id}",
                     response_model=JSENDOutSchema[HostelAccomodationViewOut], tags=["Student dashboard"])
async def read_hostel_accommodation(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_hostel_accommodation(university_id, user_request_id),
        "message": "Get hostel accommodation"
    }


@services_router.get("/{university_id}/user-request/{user_request_id}", response_model=JSENDOutSchema[UserRequestDetailsViewOut],
                     tags=["Student dashboard"])
async def read_request_details(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_request_details(university_id, user_request_id),
        "message": "Got request details"
    }