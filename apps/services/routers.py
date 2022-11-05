from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.services.handlers import service_handler
from apps.services.schemas import UserRequestExistenceOut, UserRequestsListOut, CreateUserRequestOut, \
    CreateUserRequestIn, UserRequestBookingHostelOut, CancelRequestOut, CancelRequestIn, UserRequestReviewOut, \
    UserRequestReviewIn, HostelAccomodationViewOut, UserRequestDetailsViewOut

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


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
                     tags=["Student dashboard"])
async def check_user_request_existence(
        request: Request,
        university_id: int,
        service_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):  # TODO: nothing prevents student from creating multiple requests with the same id
    """
    **Checking user request existence**

    **Path**
    - **university_id**: user university id
    - **service_id**: id of the service requested by the student

    **Return**: user request id; user request status; user request existence
    """
    return {
        "data": await service_handler.read_user_request_existence(
            request=request,
            university_id=university_id,
            service_id=service_id,
            user=user,
            session=session
        ),
        "message": "Got user request existence"
    }


@services_router.get("/{university_id}/user-request/",
                     name="read_user_request_list",
                     response_model=JSENDOutSchema[List[UserRequestsListOut]],
                     summary="Get user request list",
                     responses={200: {"description": "Successful get university user request list response"}},
                     tags=["Student dashboard"])
async def read_user_request_list(
        request: Request,
        university_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return {
        "data": await service_handler.read_user_request_list(
            request=request,
            university_id=university_id,
            user=user,
            session=session
        ),
        "message": "Got user requests list"
    }


@services_router.post("/{university_id}/user-request/",
                      name="create_user_request",
                      response_model=JSENDOutSchema[CreateUserRequestOut],
                      summary="Create user request",
                      responses={200: {"description": "Successful create user request response"}},
                      tags=["Student dashboard"])
async def create_user_request(
        request: Request,
        university_id: int,
        user_request: CreateUserRequestIn,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    **Create user request**

    **Path**:
    - **university_id**: user university id

    **Input**:
    - **service_id**: service id, required
    - **comment**: comment for the creating user request

    **Return**: user request id; request status id
    """
    response = await service_handler.create_user_request(
        request=request,
        university_id=university_id,
        user_request=user_request,
        user=user,
        session=session
    )
    return {
        "data": response,
        "message": f"Created user request with id {response['user_request_id']}"
    }


@services_router.get("/{university_id}/user-request-booking-hostel/",
                     name="read_user_request_booking_hostel",
                     response_model=JSENDOutSchema[UserRequestBookingHostelOut],
                     summary="Get user request booking hostel",
                     responses={200: {"description": "Successful get user request booking hostel response"}},
                     tags=["Student dashboard"])
async def read_user_request_booking_hostel(
        request: Request,
        university_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    return {
        "data": await service_handler.read_user_request_booking_hostel(
            request=request,
            university_id=university_id,
            user=user,
            session=session),
        "message": "Got user request booking hostel"
    }


@services_router.put("/{university_id}/user-request/{user_request_id}",
                     name="update_cancel_user_request",
                     response_model=JSENDOutSchema[CancelRequestOut],
                     summary="Cancel user request",
                     responses={200: {"description": "Successful cancel user request response"}},
                     tags=["Student dashboard"])
async def cancel_request(
        request: Request,
        university_id: int,
        user_request_id: int,
        cancel_request: CancelRequestIn,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    """
    **Cancel user request**

    **Path**:
    - **university_id**: user university id
    - **user_request_id**: user request id

    **Input**:
    - **status_id**: user request status id, required

    **Return**: canceled user request id and status id
    """
    return {
        "data": await service_handler.cancel_request(
            request=request,
            user_request_id=user_request_id,
            cancel_request=cancel_request,
            session=session),
        "message": f"Canceled request with id {user_request_id}"
    }


@services_router.post("/{university_id}/user-request-review/{user_request_id}/",
                      name="create_user_request_review",
                      response_model=JSENDOutSchema[UserRequestReviewOut],
                      summary="Create user request review",
                      responses={200: {"description": "Successful create user request review response"}},
                      tags=["Admin dashboard"])
async def create_user_request_review(
        request: Request,
        university_id: int,
        user_request_id: int,
        user_request_review: UserRequestReviewIn,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    """
        **Create user request review**

        **Path**:
        - **university_id**: user university id
        - **user_request_id**: user request id

        **Input**:
        - **status_id**: user request status id, required
        - **room_number**: user room number
        - **start_date_accommodation**: starting datetime hostel accommodation
        - **end_date_accommodation**: end datetime hostel accommodation
        - **total_sum**: total sum of hostel accommodation payment
        - **payment_deadline**: deadline datetime for hostel accommodation payment
        - **remark**: additional info for request review
        - **hostel_id**: hostel id in the database
        - **bed_place_id**: hostel bed place id

        **Return**: user request status id; user request review id
    """
    return {
        "data": await service_handler.create_user_request_review(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            user_request_review=user_request_review,
            user=user,
            session=session),
        "message": "Created user request review"
    }


@services_router.get("/{university_id}/hostel-accommodation/{user_request_id}",
                     name="read_hostel_accommodation",
                     response_model=JSENDOutSchema[HostelAccomodationViewOut],
                     summary="Get hostel accommodation",
                     responses={200: {"description": "Successful get user request hostel accommodation response"}},
                     tags=["Student dashboard"])
async def read_hostel_accommodation(
        request: Request,
        university_id: int,
        user_request_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    return {
        "data": await service_handler.read_hostel_accommodation(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            session=session),
        "message": "Get hostel accommodation"
    }


@services_router.get("/{university_id}/user-request/{user_request_id}",
                     name="read_user_request_details",
                     response_model=JSENDOutSchema[UserRequestDetailsViewOut],
                     summary="Get user request",
                     responses={200: {"description": "Successful get user request response"}},
                     tags=["Student dashboard"])   # TODO Return Validation error with empty data
async def read_request_details(
        request: Request,
        university_id: int,
        user_request_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    return {
        "data": await service_handler.read_request_details(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            session=session),
        "message": "Got request details"
    }