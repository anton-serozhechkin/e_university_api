from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.db import database
from apps.common.services import AsyncCRUDBase
from apps.educational_institutions.models import Faculty, Speciality
from apps.hostel.models import BedPlace, Hostel
from apps.services.models import (
    Service,
    UserDocument,
    UserRequest,
    UserRequestReview,
    hostel_accommodation_view,
    user_documents_list_view,
    user_request_booking_hostel_view,
    user_request_details_view,
    user_request_exist_view,
    user_request_hostel_accommodation_warrant_view,
    user_request_list_view,
)
from apps.users.models import UserFaculty


async def get_specialties_list(session: AsyncSession, university_id: int) -> List:
    result = await session.execute(
        select(
            Faculty.faculty_id,
            Faculty.shortname,
            Speciality.speciality_id,
            Speciality.name,
        )
        .filter(Speciality.faculty_id == Faculty.faculty_id)
        .where(Faculty.university_id == university_id)
    )
    return result.all()


bed_place_service = AsyncCRUDBase(model=BedPlace)
hostel_service = AsyncCRUDBase(model=Hostel)
request_existence_service = AsyncCRUDBase(model=user_request_exist_view)
service_service = AsyncCRUDBase(model=Service)
user_request_list_service = AsyncCRUDBase(model=user_request_list_view)
user_faculty_service = AsyncCRUDBase(model=UserFaculty)
user_request_service = AsyncCRUDBase(model=UserRequest)
user_request_booking_hostel_service = AsyncCRUDBase(
    model=user_request_booking_hostel_view
)
user_request_review_service = AsyncCRUDBase(model=UserRequestReview)
user_documents_list_service = AsyncCRUDBase(model=user_documents_list_view)
hostel_accommodation_service = AsyncCRUDBase(model=hostel_accommodation_view)
user_request_detail_service = AsyncCRUDBase(model=user_request_details_view)
user_document_service = AsyncCRUDBase(model=UserDocument)
user_request_hostel_accommodation_warrant_view_service = AsyncCRUDBase(
    model=user_request_hostel_accommodation_warrant_view
)
