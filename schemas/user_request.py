from datetime import date, datetime


from pydantic import BaseModel


class CreateUserRequestIn(BaseModel):
    service_id: int
    comment: str = None


class CreateUserRequestOut(BaseModel):
    user_request_id: int
    status_id: int


class UserRequestExistenceOut(BaseModel):
    user_request_id: int = None
    status_id: int = None
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


class UserRequestsListOut(BaseModel):
    university_id: int
    user_id: int
    user_request_id: int
    service_name: str
    status_name: str
    date_created: datetime
