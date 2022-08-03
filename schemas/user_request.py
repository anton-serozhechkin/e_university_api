from datetime import date, datetime
from typing import Dict, Union


from pydantic import BaseModel, validator


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
    speciality_code: int = None # delete it after table speciality won't be empty
    speciality_name: str = None # delete it after table speciality won't be empty
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
            message = "Заяву можливо тільки скасувати."
            raise ValueError(message)
        return v


class CancelRequestOut(BaseModel):
    user_request_id: int
    status_id: int


class HostelAccomodationViewOut(BaseModel):
    university_id: int
    user_request_review_id: int
    user_request_id: int
    hostel_name: Dict[str, Union[int, str]]
    hostel_address: Dict[str, str]
    bed_place_name: str
    month_price: float
    start_date_accommodation: datetime
    end_date_accommodation: datetime
    total_sum: float
    iban: str
    university_name: str
    organisation_code: str
    payment_recognation: str
    commandant_full_name: str
    telephone_number: str
    documents: Dict[str, str]
 