from apps.common.file_managers import file_manager
from apps.services.models import STATUS_MAPPING, UserDocument
from apps.services.schemas import (CancelRequestIn, CreateUserRequestIn, CountHostelAccommodationCostIn,
                                   HostelAccomodationViewOut, UserRequestBookingHostelOut, UserRequestDetailsViewOut,
                                   UserRequestsListOut, UserRequestReviewIn)
from apps.services.services import (
    hostel_accommodation_service, request_existence_service, user_request_list_service,
    user_faculty_service, user_request_service, user_request_booking_hostel_service, user_request_review_service,
    user_request_detail_service, hostel_service, bed_place_service, user_document_service, service_service
)
from apps.users.schemas import UserOut
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH, HOSTEL_BOOKING_TEMPLATE)

from datetime import datetime, date
from decimal import Decimal
from fastapi import Request
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Union


class ServiceHandler:

    @staticmethod
    async def read_user_request_existence(
            *,
            request: Request,
            university_id: int,
            service_id: int,
            user: UserOut,
            session: AsyncSession
    ) -> Dict[str, Union[bool, int, None]]:
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

    @staticmethod
    async def read_user_request_list(
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ) -> List[UserRequestsListOut]:
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
    ) -> Dict[str, int]:
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
        await self.__create_user_document(session, **prepared_data)
        return {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": user_request.user_request_id
        }

    @staticmethod
    async def read_user_request_booking_hostel(
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ) -> UserRequestBookingHostelOut:
        return await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id})

    @staticmethod
    async def cancel_request(
            *,
            request: Request,
            user_request_id: int,
            cancel_request: CancelRequestIn,
            session: AsyncSession) -> Dict[str, int]:
        CancelRequestIn(status_id=cancel_request.status_id)
        await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj=cancel_request)
        return {
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        }

    @staticmethod
    async def create_user_request_review(
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            user_request_review: UserRequestReviewIn,
            user: UserOut,
            session: AsyncSession) -> Dict[str, int]:
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

    @staticmethod
    async def read_hostel_accommodation(
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession) -> HostelAccomodationViewOut:
        response = await hostel_accommodation_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })
        # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's happened only if user request doesn't have review)
        return response

    @staticmethod
    async def read_request_details(
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession) -> UserRequestDetailsViewOut:
        return await user_request_detail_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })

    @staticmethod
    async def read_user_document(
            *,
            request: Request,
            university_id: int,
            user_document_id: int,
            user: UserOut,
            session: AsyncSession) -> str:
        user_document = await user_document_service.read(session=session, data={"user_document_id": user_document_id})
        return file_manager.get(user_document.content)

    async def count_hostel_accommodation_cost(
            self,
            *,
            request: Request,
            university_id: int,
            data: CountHostelAccommodationCostIn,
            session: AsyncSession) -> Dict[str, Decimal]:
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
        return (end_date.month - start_date.month + 12 * (end_date.year - start_date.year)) + 1

    @classmethod
    def get_month_price_by_bed_place(cls, hostel_month_price: Decimal, bed_place_name: str) -> Decimal:
        return Decimal(hostel_month_price) * Decimal(bed_place_name)

    @classmethod
    def calculate_total_hostel_accommodation_cost(cls, month_price: Decimal, month_difference: int) -> Decimal:
        return month_price * month_difference

    @classmethod
    async def __create_user_document(cls, session: AsyncSession, **kwargs) -> UserDocument:
        service_id = kwargs.get("service_id")
        name = await cls.__generate_user_document_name(service_id, session)
        date_created = datetime.strptime(datetime.now().strftime(Settings.DATETIME_FORMAT),
                                         Settings.DATETIME_FORMAT)
        kwargs["date_created"] = date_created
        content = await cls.__create_user_document_content_hostel_settlement_service(**kwargs)
        user_document_record = await user_document_service.create(
            session=session,
            data={
                "date_created": date_created,
                "name": name,
                "content": content,
                "user_request_id": kwargs.get("user_request_id")
            })
        return user_document_record

    @classmethod
    async def __create_user_document_content_hostel_settlement_service(cls, **kwargs) -> str:
        context = kwargs.get("context")
        rendered_template = file_manager.render(TEMPLATES_PATH, HOSTEL_BOOKING_TEMPLATE, context)
        file_date_created = str(kwargs.get('date_created')).replace(":", "-").replace(" ", "_")
        document_name = f"hostel_settlement_{file_date_created}_{kwargs.get('user_request_id')}.docx"
        DOCUMENT_PATH = SETTLEMENT_HOSTEL_PATH / str(context.user_id)
        Path(DOCUMENT_PATH).mkdir(exist_ok=True)
        document_path = file_manager.create(DOCUMENT_PATH, document_name, rendered_template)
        return document_path

    @classmethod
    async def __generate_user_document_name(cls, service_id: int, session: AsyncSession) -> str:
        service = await service_service.read(
            session=session,
            data={"service_id": service_id}
        )
        return f"Заява на {service.service_name.lower()}"


service_handler = ServiceHandler()
