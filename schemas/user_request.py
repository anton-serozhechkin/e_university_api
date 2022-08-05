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

class UserRequestReviewIn(BaseModel):
    status_id: int
    room_number: int = None
    start_date_accommodation: datetime = None
    end_date_accommodation: datetime = None
    total_sum: float = None
    payment_deadline: datetime = None
    remark: str = None
    hostel_id: int = None
    bed_place_id: int = None

    @validator('status_id')
    def validate_status_id(cls, v):
        if v not in [1,2]:
            message = "Заяву можливо тільки ухвалити або відхилити."
            raise ValueError(message)
        return v

class UserRequestReviewOut(BaseModel):
    status_id: int
    user_request_review_id: int
