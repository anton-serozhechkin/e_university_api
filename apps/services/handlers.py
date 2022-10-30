from apps.common.db import database
from apps.services.models import user_request_exist_view, user_request_list_view, STATUS_MAPPING, UserRequest, \
    user_request_booking_hostel_view, UserRequestReview, hostel_accommodation_view, user_request_details_view
from apps.services.schemas import CreateUserRequestIn, CancelRequestIn, UserRequestExistenceOut, UserRequestReviewIn
from apps.services.services import create_user_document, request_existence_service
from apps.users.models import UserFaculty
from apps.users.schemas import UserOut

from fastapi import Request
from datetime import datetime
import json

from sqlalchemy import select, insert, update
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
        user_request_result = await request_existence_service.read_mod(
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

    async def read_user_request_list(university_id: int, user: UserOut):
        query = select(user_request_list_view).where(user_request_list_view.c.user_id == user.user_id,
                                                     user_request_list_view.c.university_id == university_id)
        return await database.fetch_all(query)

    async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user: UserOut):
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
        query = select(user_request_booking_hostel_view).where(
            user_request_booking_hostel_view.c.user_id == user.user_id,
            user_request_booking_hostel_view.c.university_id == university_id
        )
        result = await database.fetch_one(query)

        prepared_data = {
            "context": result,
            "service_id": user_request.service_id,
            "user_request_id": last_record_id
        }
        await create_user_document(**prepared_data)
        return {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": last_record_id
        }

    async def read_user_request_booking_hostel(university_id: int, user: UserOut):
        query = select(user_request_booking_hostel_view).where(
            user_request_booking_hostel_view.c.user_id == user.user_id,
            user_request_booking_hostel_view.c.university_id == university_id
        )
        return await database.fetch_one(query)

    async def cancel_request(user_request_id: int, cancel_request: CancelRequestIn):
        CancelRequestIn(status_id=cancel_request.status_id)
        query = update(UserRequest).where(UserRequest.user_request_id == user_request_id).values(
            status_id=cancel_request.status_id)
        await database.execute(query)
        return {
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        }

    async def create_user_request_review(university_id: int, user_request_id: int, user_request_review: UserRequestReviewIn,
                                         user: UserOut):
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

        query = update(UserRequest).values(status_id=user_request_review.status_id).where(
            UserRequest.user_request_id == user_request_id
        )
        await database.execute(query)

        return {
            "status_id": user_request_review.status_id,
            "user_request_review_id": last_record_id
        }

    async def read_hostel_accommodation(university_id: int, user_request_id: int):
        query = select(hostel_accommodation_view).where(hostel_accommodation_view.c.university_id == university_id,
                                                        hostel_accommodation_view.c.user_request_id == user_request_id)
        response = await database.fetch_one(query)

        response.documents = json.loads(response.documents)
        # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's heppend only if user request doesn't have review)

        response.hostel_name = json.loads(response.hostel_name)
        response.hostel_address = json.loads(response.hostel_address)
        return response

    async def read_request_details(university_id: int, user_request_id: int):
        query = select(user_request_details_view).where(user_request_details_view.c.university_id == university_id,
                                                        user_request_details_view.c.user_request_id == user_request_id)

        response = await database.fetch_one(query)

        response.documents = json.loads(response.documents)
        response.hostel_name = json.loads(response.hostel_name)
        return response


service_handler = ServiceHandler()
