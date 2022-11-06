from decimal import Decimal

from apps.common.db import database
from apps.common.services import AsyncCRUDBase
from apps.hostel.models import Hostel, BedPlace
from apps.services.models import (
    hostel_accommodation_view, Service, UserDocument, user_request_exist_view, user_request_list_view,
    UserRequest, user_request_booking_hostel_view, UserRequestReview, user_request_details_view
)
from apps.users.models import UserFaculty
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH)

from datetime import datetime, date
from docxtpl import DocxTemplate
from sqlalchemy import select, insert

HOSTEL_BOOKING_TEMPLATE_URL = "hostel_booking_template.docx"


async def generate_document_name(service_id: int) -> str:
    query = select(Service).where(Service.service_id == service_id)
    query_result = await database.fetch_one(query)
    return f"Заява на {query_result.service_name.lower()}"


async def create_user_document_content(**kwargs) -> str:
    if kwargs.get("service_id") == 1:
        path_to_template = TEMPLATES_PATH / HOSTEL_BOOKING_TEMPLATE_URL
        doc = DocxTemplate(path_to_template)
        context = kwargs.get("context")
        doc.render(context)
        document_name = f"hostel_settlement_{kwargs.get('date_created')}_{kwargs.get('user_request_id')}.docx"
        path_to_storage = SETTLEMENT_HOSTEL_PATH / document_name.replace(":", "_")
        doc.save(path_to_storage)
        return str(path_to_storage)
    raise RuntimeError(f"create_user_document_content({kwargs}) | there is no service_id!!!")


async def create_user_document(**kwargs):
    service_id = kwargs.get("service_id")
    name = await generate_document_name(service_id)
    date_created = datetime.strptime(datetime.now().strftime(Settings.DATETIME_FORMAT),
                                     Settings.DATETIME_FORMAT)
    kwargs["date_created"] = date_created
    content = await create_user_document_content(**kwargs)
    query = insert(UserDocument).values(date_created=date_created,
                                        name=name,
                                        content=content,
                                        user_request_id=kwargs.get("user_request_id"))
    result = await database.execute(query)
    return result


def calculate_difference_between_dates_in_months(end_date: date, start_date: date) -> int:
    return end_date.month - start_date.month + 12 * (end_date.year - start_date.year)


def get_month_price_by_bed_place(hostel_month_price: Decimal, bed_place_name: str) -> Decimal:
    return Decimal(hostel_month_price) * Decimal(bed_place_name)


def calculate_total_hostel_accommodation_cost(month_price: Decimal, month_difference: int) -> Decimal:
    return month_price * month_difference


request_existence_service = AsyncCRUDBase(model=user_request_exist_view)
user_request_list_service = AsyncCRUDBase(model=user_request_list_view)
user_faculty_service = AsyncCRUDBase(model=UserFaculty)
user_request_service = AsyncCRUDBase(model=UserRequest)
user_request_booking_hostel_service = AsyncCRUDBase(model=user_request_booking_hostel_view)
user_request_review_service = AsyncCRUDBase(model=UserRequestReview)
hostel_accommodation_service = AsyncCRUDBase(model=hostel_accommodation_view)
user_request_detail_service = AsyncCRUDBase(model=user_request_details_view)
hostel_service = AsyncCRUDBase(model=Hostel)
bed_place_service = AsyncCRUDBase(model=BedPlace)
