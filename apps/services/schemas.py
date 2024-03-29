from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Union

from pydantic import root_validator, validator

from apps.common.schemas import (
    BaseInSchema,
    BaseOutSchema,
    FullNameSchema,
    HostelNameSchema,
    UserDocumentsSchema,
)


class CreateUserRequestIn(BaseInSchema):
    service_id: int
    comment: str = None


class CreateUserRequestOut(BaseOutSchema):
    user_request_id: int
    created_at: datetime
    comment: str = None
    user_id: int
    service_id: int
    faculty_id: int
    university_id: int
    status_id: int


class UserRequestExistenceOut(BaseOutSchema):
    user_request_id: int = None
    status: Dict[str, Union[int, str]] = None
    user_request_exist: bool = False


class UserRequestBookingHostelOut(BaseOutSchema):
    full_name: FullNameSchema
    user_id: int
    faculty_name: str
    university_id: int
    short_university_name: str
    rector_full_name: FullNameSchema
    date_today: date
    start_year: int
    finish_year: int
    speciality_code: int
    speciality_name: str
    course: int
    educ_level: str
    gender: str


class UserDocumenstListOut(BaseOutSchema):
    university_id: int
    user_document_id: int
    name: str
    created_at: datetime
    updated_at: datetime


class UserRequestsListOut(BaseOutSchema):
    university_id: int
    user_id: int
    user_request_id: int
    service_name: str
    status: Dict[str, Union[int, str]]
    created_at: datetime


class CancelRequestIn(BaseInSchema):
    status_id: int

    @validator("status_id")
    def validate_status_id(cls, v: int) -> int:
        if v != 4:
            raise ValueError("The application can only be canceled")
        return v


class UserRequestReviewIn(BaseInSchema):
    status_id: int
    room_number: int = None
    start_accommodation_date: date = None
    end_accommodation_date: date = None
    # TODO it's define as decimal, but return int
    total_sum: Decimal = None
    payment_deadline_date: date = None
    remark: str = None
    hostel_id: int = None
    bed_place_id: int = None

    @validator("status_id")
    def validate_status_id(cls, v: int) -> int:
        if v not in [1, 2]:
            raise ValueError("The application can only be approved or rejected")
        return v


class UserRequestReviewOut(BaseOutSchema):
    user_request_review_id: int
    created_at: datetime
    room_number: int = None
    start_accommodation_date: date = None
    end_accommodation_date: date = None
    total_sum: Decimal = None
    payment_deadline_date: date = None
    remark: str = None
    bed_place_id: int = None
    reviewer: int
    hostel_id: int = None
    university_id: int
    user_request_id: int


class HostelAccomodationViewOut(BaseOutSchema):
    university_id: int
    user_request_review_id: int
    user_request_id: int
    hostel_name: Dict[str, Union[int, str]]
    hostel_address: Dict[str, str]
    bed_place_name: str
    # TODO it's define as decimal, but return int
    month_price: Decimal
    start_accommodation_date: date
    end_accommodation_date: date
    # TODO it's define as decimal, but return int
    total_sum: Decimal
    iban: str
    university_name: str
    organisation_code: str
    payment_recognition: str
    commandant_full_name: FullNameSchema
    telephone_number: str
    documents: Dict[str, str]


class UserRequestDetailsViewOut(BaseOutSchema):
    user_request_id: int
    university_id: int
    created_at: datetime
    service_name: str
    status_name: str
    status_id: int
    comment: str = None
    hostel_name: HostelNameSchema
    room_number: int = None
    bed_place_name: str = None
    remark: str = None
    documents: List[UserDocumentsSchema]


class CountHostelAccommodationCostIn(BaseInSchema):
    hostel_id: int
    start_accommodation_date: date
    end_accommodation_date: date
    bed_place_id: int

    @root_validator
    def validate_two_dates(cls, values: Dict) -> Dict:
        if values.get("start_accommodation_date") >= values.get(
            "end_accommodation_date"
        ):
            raise ValueError(
                "Start date of hostel accommodation can't be more or equal than end"
                " date of hostel accommodation"
            )
        return values


class CountHostelAccommodationCostOut(BaseOutSchema):
    total_hostel_accommodation_cost: Decimal


class UserRequestHostelAccommodationWarrantViewOut(BaseOutSchema):
    user_request_review_id: int
    room_number: int
    user_request_id: int
    created_at: datetime
    hostel_number: int
    hostel_street: str
    hostel_build: str
    bed_place_name: str
    university_name: str
    short_university_name: str
    university_city: str
    status_id: int
    user_id: int
    student_full_name: FullNameSchema
    student_gender: str
    faculty_shortname: str
    dean_full_name: FullNameSchema
