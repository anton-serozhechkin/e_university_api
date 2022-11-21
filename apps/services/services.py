from apps.common.db import database
from apps.common.services import AsyncCRUDBase
from apps.educational_institutions.models import Faculty, Speciality

from apps.hostel.models import Hostel, BedPlace
from apps.services.models import (
    hostel_accommodation_view, Service, UserDocument, user_request_exist_view, user_request_list_view,
    UserRequest, user_request_booking_hostel_view, UserRequestReview, user_request_details_view
)
from apps.users.models import UserFaculty
from sqlalchemy import select, insert


async def get_specialties_list(university_id):
    query = select(Faculty, Speciality).filter(
        Speciality.faculty_id == Faculty.faculty_id
    ).where(Faculty.university_id == university_id)
    return await database.fetch_all(query)


request_existence_service = AsyncCRUDBase(model=user_request_exist_view)
user_request_list_service = AsyncCRUDBase(model=user_request_list_view)
user_faculty_service = AsyncCRUDBase(model=UserFaculty)
user_request_service = AsyncCRUDBase(model=UserRequest)
user_request_booking_hostel_service = AsyncCRUDBase(model=user_request_booking_hostel_view)
user_request_review_service = AsyncCRUDBase(model=UserRequestReview)
hostel_accommodation_service = AsyncCRUDBase(model=hostel_accommodation_view)
user_request_detail_service = AsyncCRUDBase(model=user_request_details_view)
user_document_service = AsyncCRUDBase(model=UserDocument)
hostel_service = AsyncCRUDBase(model=Hostel)
bed_place_service = AsyncCRUDBase(model=BedPlace)
service_service = AsyncCRUDBase(model=Service)
