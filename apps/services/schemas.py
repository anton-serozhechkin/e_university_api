from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Union, List

from pydantic import BaseModel, validator, root_validator


class CreateUserRequestIn(BaseModel):
    service_id: int
    comment: str = None


class CreateUserRequestOut(BaseModel):
    user_request_id: int
    status_id: int


class UserRequestExistenceOut(BaseModel):
    user_request_id: int = None
    status: Dict[str, Union[int, str]] = None
    user_request_exist: bool


class UserRequestBookingHostelOut(BaseModel):
    full_name: str
    user_id: int
    faculty_name: str
    university_id: int
    short_university_name: str
    rector_full_name: str
    date_today: date
    start_year: int
    finish_year: int
    speciality_code: int = None  # delete it after table speciality won't be empty
    speciality_name: str = None  # delete it after table speciality won't be empty
    course: int
    educ_level: str
    gender: str


class UserRequestsListOut(BaseModel):
    university_id: int
    user_id: int
    user_request_id: int
    service_name: str
    status: Dict[str, Union[int, str]]
    date_created: datetime


class CancelRequestIn(BaseModel):
    status_id: int

    @validator('status_id')
    def validate_status_id(cls, v):
        if v != 4:
            raise ValueError("The application can only be canceled.")
        return v


class CancelRequestOut(BaseModel):
    user_request_id: int
    status_id: int


class UserRequestReviewIn(BaseModel):
    status_id: int
    room_number: int = None
    start_date_accommodation: datetime = None
    end_date_accommodation: datetime = None
    # TODO it's define as decimal, but return int
    total_sum: Decimal = None
    payment_deadline: datetime = None
    remark: str = None
    hostel_id: int = None
    bed_place_id: int = None

    @validator('status_id')
    def validate_status_id(cls, v):
        if v not in [1, 2]:
            raise ValueError("The application can only be approved or rejected.")
        return v


class UserRequestReviewOut(BaseModel):
    status_id: int
    user_request_review_id: int


class HostelAccommodationViewOut(BaseModel):
    university_id: int
    user_request_review_id: int
    user_request_id: int
    hostel_name: Dict[str, Union[int, str]]
    hostel_address: Dict[str, str]
    bed_place_name: str
    # TODO it's define as decimal, but return int
    month_price: Decimal
    start_date_accommodation: datetime
    end_date_accommodation: datetime
    # TODO it's define as decimal, but return int
    total_sum: Decimal
    iban: str
    university_name: str
    organisation_code: str
    payment_recognation: str  # TODO spelling error
    commandant_full_name: str
    telephone_number: str
    documents: Dict[str, str]


class UserRequestDetailsViewOut(BaseModel):
    user_request_id: int
    university_id: int
    date_created: datetime
    service_name: str
    status_name: str
    status_id: int
    comment: str = None
    hostel_name: Dict[str, Union[int, str]] = None
    room_number: int = None
    bed_place_name: str = None
    date_review: datetime = None
    remark: str = None
    documents: List[Dict[str, str]]


class CountHostelAccommodationCostIn(BaseModel):
    hostel_id: int
    start_date_accommodation: date
    end_date_accommodation: date
    bed_place_id: int

    @root_validator
    def validate_two_dates(cls, values):
        if values.get('start_date_accommodation') >= values.get('end_date_accommodation'):
            raise ValueError(
                "Start date of hostel accommodation can't be more or equal than end date of hostel accommodation"
            )
        return values


class CountHostelAccommodationCostOut(BaseModel):
    total_hostel_accommodation_cost: Decimal
