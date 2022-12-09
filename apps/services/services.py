from apps.common.services import AsyncCRUDBase
from apps.hostel.models import Hostel, BedPlace
from apps.services.models import (
    hostel_accommodation_view, Service, UserDocument, user_request_exist_view, user_request_list_view,
    UserRequest, user_request_booking_hostel_view, UserRequestReview, user_request_details_view, return_user_document_view
)
from apps.users.models import UserFaculty


request_existence_service = AsyncCRUDBase(model=user_request_exist_view)
user_request_list_service = AsyncCRUDBase(model=user_request_list_view)
user_faculty_service = AsyncCRUDBase(model=UserFaculty)
user_request_service = AsyncCRUDBase(model=UserRequest)
user_request_booking_hostel_service = AsyncCRUDBase(model=user_request_booking_hostel_view)
user_request_review_service = AsyncCRUDBase(model=UserRequestReview)
hostel_accommodation_service = AsyncCRUDBase(model=hostel_accommodation_view)
user_request_detail_service = AsyncCRUDBase(model=user_request_details_view)
user_document_service = AsyncCRUDBase(model=UserDocument)
return_user_document = AsyncCRUDBase(model=return_user_document_view)
hostel_service = AsyncCRUDBase(model=Hostel)
bed_place_service = AsyncCRUDBase(model=BedPlace)
service_service = AsyncCRUDBase(model=Service)
