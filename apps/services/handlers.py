from apps.common.db import database
from apps.common.exceptions import BackendException
from apps.common.file_manager import file_manager
from apps.services.models import user_request_exist_view, user_request_list_view, STATUS_MAPPING, UserRequest, \
    user_request_booking_hostel_view, UserRequestReview, hostel_accommodation_view, user_request_details_view,\
    UserDocument
from apps.services.schemas import UserRequestExistenceOut, UserRequestsListOut, CreateUserRequestOut, \
    CreateUserRequestIn, UserRequestBookingHostelOut, CancelRequestOut, CancelRequestIn, UserRequestReviewOut, \
    UserRequestReviewIn, HostelAccomodationViewOut, UserRequestDetailsViewOut
from apps.services.services import create_user_document
from apps.users.handlers import get_current_user
from apps.users.models import UserFaculty
from apps.services.models import STATUS_MAPPING
from apps.services.schemas import CancelRequestIn, CreateUserRequestIn, UserRequestReviewIn
from apps.services.services import (
    create_user_document, hostel_accommodation_service, request_existence_service, user_request_list_service,
    user_faculty_service, user_request_service, user_request_booking_hostel_service, user_request_review_service,
    user_request_detail_service
)
from apps.users.schemas import UserOut

from datetime import datetime
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


@services_router.get("/{university_id}/service-document/{user_request_id}",
                     name="read_service_document",
                     response_class=StreamingResponse,
                     summary="Read service document",
                     responses={200: {
                         "description": "Successful get service document response",
                         "content": {"text/html": {"example": "bytes"}}
                     }},
                     tags=["Admin dashboard", "Student dashboard"])
async def read_service_document(university_id: int, user_request_id: int, user=Depends(get_current_user)):
    if user.university_id != university_id:
        raise BackendException(
            message="Access denied. May be input is not correct",
            code=http_status.HTTP_403_FORBIDDEN
        )
    query = select(UserDocument).where(UserDocument.user_request_id == user_request_id)

    user_document = await database.fetch_one(query)

    return StreamingResponse(
        content=file_manager.get(user_document.content),
        status_code=http_status.HTTP_200_OK,
        media_type="text/html"
    )
