from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Union, Optional

from pydantic import root_validator, validator

from apps.common.schemas import (
    BaseInSchema,
    BaseOutSchema,
    FullNameSchema,
    HostelNameSchema,
    UserDocumentsSchema,
)


class RequestForHostelAccommodationIn(BaseInSchema):
    rector_first_name: str
    rector_middle_name: str = None
    rector_last_name: str
    student_first_name: str
    student_middle_name: str = None
    student_last_name: str
    speciality_code: int
    speciality_name: str
    course: int
    faculty_name: str
    educ_level: str
    comment: str = None

    @root_validator
    def validate_rector_and_student_names(cls, values: str) -> str:
        names = [
            "rector_first_name",
            "rector_last_name",
            "student_first_name",
            "student_last_name",
        ]
        for name in names:
            if not values.get(name).istitle():
                raise ValueError(
                    f"{name.replace('_', ' ').capitalize()} first letter must be uppercase"
                )
        return values

    @validator("student_middle_name")
    def validate_student_middle_name(cls, value: str) -> Optional[str]:
        if value:
            if not value.istitle():
                raise ValueError("Middle name must be uppercase")
            return value
        return value

    @validator("rector_middle_name")
    def validate_rector_middle_name(cls, value: str) -> Optional[str]:
        if value:
            if not value.istitle():
                raise ValueError("Middle name must be uppercase")
            return value
        return value

    @validator("educ_level")
    def validate_education_level(cls, value: str) -> str:
        if value.upper() not in ["B", "M"]:
            raise ValueError("Wrong education level value. Should be 'B' or 'M'")
        return value

    @validator("course")
    def validate_course(cls, value: int) -> int:
        if value not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"Wrong '{value}' number. This course doesn't exist")
        return value


class RequestForHostelAccommodationOut(BaseOutSchema):
    user_request_id: int
    created_at: datetime
    comment: str = None
    user_id: int
    service_id: int
    faculty_id: int
    university_id: int
    status_id: int


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
