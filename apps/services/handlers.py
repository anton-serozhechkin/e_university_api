from apps.common.exceptions import BackendException
from apps.common.file_manager import file_manager
from apps.services.models import STATUS_MAPPING
from apps.services.schemas import CancelRequestIn, CreateUserRequestIn, UserRequestReviewIn, \
    CountHostelAccommodationCostIn
from apps.services.services import (
    create_user_document, hostel_accommodation_service, request_existence_service, user_request_list_service,
    user_faculty_service, user_request_service, user_request_booking_hostel_service, user_request_review_service,
    user_request_detail_service, hostel_service, bed_place_service, user_document_service
)
from apps.users.schemas import UserOut

from datetime import datetime, date
from decimal import Decimal
from fastapi import Request, status as http_status
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
        # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's happened only if user request doesn't have review)
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

    async def read_service_document(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            user: UserOut,
            session: AsyncSession):
        if user.university_id != university_id:
            raise BackendException(
                message="Access denied. May be input is not correct",
                code=http_status.HTTP_403_FORBIDDEN
            )
        user_document = await user_document_service.read(session=session, data={"user_request_id": user_request_id})
        return file_manager.get(user_document.content)

    async def count_hostel_accommodation_cost(
            self,
            *,
            request: Request,
            university_id: int,
            data: CountHostelAccommodationCostIn,
            session: AsyncSession):

        hostel = await hostel_service.read(
            session=session,
            data={"hostel_id": data.hostel_id}
        )

        bed_place = await bed_place_service.read(
            session=session,
            data={"bed_place_id": data.bed_place_id}
        )

        months_count = self.calculate_difference_between_dates_in_months(data.end_date_accommodation,
                                                                         data.start_date_accommodation)
        month_price = self.get_month_price_by_bed_place(hostel.month_price, bed_place.bed_place_name)

        response = self.calculate_total_hostel_accommodation_cost(month_price, months_count)
        return {
            'total_hostel_accommodation_cost': response
        }

    @classmethod
    def calculate_difference_between_dates_in_months(cls, end_date: date, start_date: date) -> int:
        return end_date.month - start_date.month + 12 * (end_date.year - start_date.year)

    @classmethod
    def get_month_price_by_bed_place(cls, hostel_month_price: Decimal, bed_place_name: str) -> Decimal:
        return Decimal(hostel_month_price) * Decimal(bed_place_name)

    @classmethod
    def calculate_total_hostel_accommodation_cost(cls, month_price: Decimal, month_difference: int) -> Decimal:
        return month_price * month_difference


service_handler = ServiceHandler()
