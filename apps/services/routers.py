from typing import List, Optional, Union

from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, StreamingResponse

from apps.common.dependencies import (
    check_file_content_type,
    get_async_session,
    get_current_user,
)
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.services.handlers import service_handler
from apps.services.schemas import (
    CancelRequestIn,
    CountHostelAccommodationCostIn,
    CountHostelAccommodationCostOut,
    CreateUserRequestIn,
    CreateUserRequestOut,
    HostelAccomodationViewOut,
    UserDocumenstListOut,
    UserRequestBookingHostelOut,
    UserRequestDetailsViewOut,
    UserRequestExistenceOut,
    UserRequestReviewIn,
    UserRequestReviewOut,
    UserRequestsListOut,
)
from apps.users.schemas import CreateStudentsListOut, UserOut

services_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@services_router.get(
    "/{university_id}/user-request-existence/{service_id}/",
    name="read_user_request_existence",
    response_model=JSENDOutSchema[UserRequestExistenceOut],
    summary="Check user request existence",
    responses={
        200: {
            "description": (
                "Successful get response with info about existence user request"
                " response"
            )
        }
    },
    tags=["Services application"],
)
async def check_user_request_existence(
    request: Request,
    university_id: int,
    service_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):  # TODO: nothing prevents student from creating multiple requests with the same id
    """**Method for checking user request existence**.

    **Path**:
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
            session=session,
        ),
        "message": "Got user request existence",
    }


@services_router.get(
    "/{university_id}/user-request/",
    name="read_user_request_list",
    response_model=JSENDOutSchema[List[UserRequestsListOut]],
    summary="Get user request list",
    responses={
        200: {"description": "Successful get university user request list response"}
    },
    tags=["Services application"],
)
async def read_user_request_list(
    request: Request,
    university_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await service_handler.read_user_request_list(
            request=request, university_id=university_id, user=user, session=session
        ),
        "message": "Got user requests list",
    }


@services_router.post(
    "/{university_id}/user-request/",
    name="create_user_request",
    response_model=JSENDOutSchema[CreateUserRequestOut],
    summary="Create user request",
    responses={200: {"description": "Successful create user request response"}},
    tags=["Services application"],
)
async def create_user_request(
    request: Request,
    university_id: int,
    user_request: CreateUserRequestIn,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for creating user request**.

    **Path**:
    - **university_id**: user university id

    **Input**:
    - **service_id**: service id, required
    - **comment**: comment for the creating user request, not required

    **Return**:
    - **user_request_id**
    - **created_at**
    - **comment**
    - **user_id**
    - **service_id**
    - **faculty_id**
    - **university_id**
    - **status_id**
    """
    response = await service_handler.create_user_request(
        request=request,
        university_id=university_id,
        user_request=user_request,
        user=user,
        session=session,
    )
    return {
        "data": response,
        "message": f"Created user request with id {response.user_request_id}",
    }


@services_router.get(
    "/{university_id}/user-request-booking-hostel/",
    name="read_user_request_booking_hostel",
    response_model=JSENDOutSchema[UserRequestBookingHostelOut],
    summary="Get user request booking hostel",
    responses={
        200: {"description": "Successful get user request booking hostel response"}
    },
    tags=["Services application"],
)
async def read_user_request_booking_hostel(
    request: Request,
    university_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await service_handler.read_user_request_booking_hostel(
            request=request, university_id=university_id, user=user, session=session
        ),
        "message": "Got user request booking hostel",
    }


@services_router.put(
    "/{university_id}/user-request/{user_request_id}",
    name="update_cancel_user_request",
    response_model=JSENDOutSchema[CreateUserRequestOut],
    summary="Cancel user request",
    responses={200: {"description": "Successful cancel user request response"}},
    tags=["Services application"],
)
async def cancel_student_request(
    request: Request,
    university_id: int,
    user_request_id: int,
    cancel_request: CancelRequestIn,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for cancel user request**.

    **Path**:
    - **university_id**: user university id
    - **user_request_id**: user request id

    **Input**:
    - **status_id**: user request status id, required

    **Return**:
    - canceled user request id
    - created at
    - comment
    - user id
    - service id
    - faculty id
    - university id
    - status id
    """
    return {
        "data": await service_handler.cancel_request(
            request=request,
            user_request_id=user_request_id,
            cancel_request=cancel_request,
            session=session,
        ),
        "message": f"Canceled request with id {user_request_id}",
    }


@services_router.post(
    "/{university_id}/user-request-review/{user_request_id}/",
    name="create_user_request_review",
    response_model=JSENDOutSchema[UserRequestReviewOut],
    summary="Create user request review",
    responses={200: {"description": "Successful create user request review response"}},
    tags=["Services application"],
)
async def create_user_request_review(
    request: Request,
    university_id: int,
    user_request_id: int,
    user_request_review: UserRequestReviewIn,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Create user request review**.

    **Path**:
    - **university_id**: user university id
    - **user_request_id**: user request id

    **Input**:
    - **status_id**: user request status id, required
    - **room_number**: user room number
    - **start_accommodation_date**: starting date hostel accommodation
    - **end_accommodation_date**: end date hostel accommodation
    - **total_sum**: total sum of hostel accommodation payment
    - **payment_deadline_date**: deadline date for hostel accommodation payment
    - **remark**: additional info for request review
    - **hostel_id**: hostel id in the database
    - **bed_place_id**: hostel bed place id

    **Return**:
    - user request status id
    - user request review id
    """
    return {
        "data": await service_handler.create_user_request_review(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            user_request_review=user_request_review,
            user=user,
            session=session,
        ),
        "message": "Created user request review",
    }


@services_router.get(
    "/{university_id}/hostel-accommodation/{user_request_id}",
    name="read_hostel_accommodation",
    response_model=JSENDOutSchema[Optional[HostelAccomodationViewOut]],
    summary="Get hostel accommodation",
    responses={
        200: {
            "description": "Successful get user request hostel accommodation response"
        }
    },
    tags=["Services application"],
)
async def read_hostel_accommodation(
    request: Request,
    university_id: int,
    user_request_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await service_handler.read_hostel_accommodation(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            session=session,
        ),
        "message": "Got hostel accommodation",
    }


@services_router.get(
    "/{university_id}/user-documents/",
    name="read_user_documents_list",
    response_model=JSENDOutSchema[Optional[List[UserDocumenstListOut]]],
    summary="Read user documents list",
    responses={200: {"description": "Successful get user documents list"}},
    tags=["Services application"],
)
async def read_user_documents_list(
    request: Request,
    university_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Read list of user documents**.

    **Path**:
    - **university_id**: user university id

    **Return**:
    - **university_id**: university id of user document
    - **user_document_id**: id of user document
    - **name**: document name
    - **created_at**: user document was created at
    - **updated_at**: user document was updated at
    """
    return {
        "data": await service_handler.read_user_documents_list(
            request=request, university_id=university_id, user=user, session=session
        ),
        "message": "Got user documents list",
    }


@services_router.get(
    "/{university_id}/user-documents/{user_document_id}",
    name="read_user_document",
    response_class=StreamingResponse,
    summary="Read user document",
    responses={
        200: {
            "description": "Successful get user document response",
            "content": {"text/html": {"example": "bytes"}},
        }
    },
    tags=["Services application"],
)
async def read_user_document(
    request: Request,
    university_id: int,
    user_document_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return StreamingResponse(
        content=await service_handler.read_user_document(
            request=request,
            university_id=university_id,
            user_document_id=user_document_id,
            user=user,
            session=session,
        ),
        status_code=http_status.HTTP_200_OK,
        media_type="text/html",
    )


@services_router.get(
    "/{university_id}/user-request/{user_request_id}",
    name="read_user_request_details",
    response_model=JSENDOutSchema[UserRequestDetailsViewOut],
    summary="Get user request",
    responses={200: {"description": "Successful get user request response"}},
    tags=["Services application"],
)  # TODO Return Validation error with empty data
async def read_request_details(
    request: Request,
    university_id: int,
    user_request_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await service_handler.read_request_details(
            request=request,
            university_id=university_id,
            user_request_id=user_request_id,
            session=session,
        ),
        "message": "Got request details",
    }


@services_router.post(
    "/{university_id}/create-students/",
    name="create_students_list_from_file",
    response_model=JSENDOutSchema[Union[List[CreateStudentsListOut], None]],
    summary="Create students list from file",
    responses={
        200: {"description": "Successful create students list from file response"}
    },
    tags=["Services application"],
)
async def create_students_list_from_file(
    request: Request,
    university_id: int,
    file: UploadFile = Depends(check_file_content_type),
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    response = await service_handler.create_students_list_from_file(
        request=request, university_id=university_id, file=file, session=session
    )
    return {"data": response, "message": "Created students list from file"}


@services_router.get(
    "/{university_id}/download-user-document/{user_document_id}",
    name="download_user_document",
    response_class=FileResponse,
    summary="Download user document",
    responses={
        200: {
            "description": "Successful download user document response",
            "content": {
                "text/html": {
                    "example": "\n".join(
                        [
                            (
                                "content-disposition: attachment;"
                                " filename*=utf-8''some_file_name.docx"
                            ),
                            "content-length: 1010",
                            (
                                "content-type:"
                                " application/vnd.openxmlformats-officedocument."
                                "wordprocessingml.document"
                            ),
                            "date: Wed,14 Dec 2022 15:58:49 GMT",
                            "etag: 9744b58c8e99ca7c251c717ad9b28bd2",
                            "last-modified: Wed,23 Nov 2022 17:49:14 GMT",
                            "server: uvicorn",
                        ]
                    )
                }
            },
        }
    },
    tags=["Services application"],
)
async def download_user_document(
    request: Request,
    university_id: int,
    user_document_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    file_path, file_name = await service_handler.download_user_document(
        request=request,
        university_id=university_id,
        user_document_id=user_document_id,
        user=user,
        session=session,
    )
    return FileResponse(
        path=file_path,
        filename=file_name,
        status_code=http_status.HTTP_200_OK,
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
    )


@services_router.post(
    "/{university_id}/count-hostel-accommodation-cost/",
    name="create_count_hostel_accommodation_cost",
    summary="Create Count Hostel Accommodation Cost",
    response_model=JSENDOutSchema[CountHostelAccommodationCostOut],
    responses={
        200: {
            "description": "Successful create count hostel accommodation cost response"
        }
    },
    tags=["Services application"],
)
async def count_hostel_accommodation_cost(
    request: Request,
    university_id: int,
    data: CountHostelAccommodationCostIn,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await service_handler.count_hostel_accommodation_cost(
            request=request, university_id=university_id, data=data, session=session
        ),
        "message": "Cost of hostel accommodation of student was counted successfully",
    }


@services_router.get(
    "/{university_id}/download-warrant-document/{user_request_review_id}/",
    name="download_warrant_document_for_hostel_accommodation",
    response_class=FileResponse,
    summary="Download warrant document for hostel accommodation",
    responses={
        200: {
            "description": "Successful download warrant document for hostel accommodation response",
            "content": {
                "text/html": {
                    "example": "\n".join(
                        [
                            (
                                "content-disposition: attachment;"
                                " filename*=utf-8''some_file_name.docx"
                            ),
                            "content-length: 1010",
                            (
                                "content-type:"
                                " application/vnd.openxmlformats-officedocument."
                                "wordprocessingml.document"
                            ),
                            "date: Wed,14 Dec 2022 15:58:49 GMT",
                            "etag: 9744b58c8e99ca7c251c717ad9b28bd2",
                            "last-modified: Wed,23 Nov 2022 17:49:14 GMT",
                            "server: uvicorn",
                        ]
                    )
                }
            },
        },
    },
    tags=["Services application"],
)
async def download_warrant_document(
    request: Request,
    university_id: int,
    user_request_review_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Download generated warrant document for student hostel accommodation**.

    **Path**:
    - **university_id**: user university id
    - **user_request_review_id**: id of user request review

    **Return**:
    - **generated file**: warrant file to download
    """
    file_path, file_name = await service_handler.download_warrant_document(
        request=request,
        user_request_review_id=user_request_review_id,
        session=session,
    )
    return FileResponse(
        path=file_path,
        filename=file_name,
        status_code=http_status.HTTP_200_OK,
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
    )
