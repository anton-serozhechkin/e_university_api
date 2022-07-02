from datetime import datetime

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


class UserRequestsListOut(BaseModel):
    university_id: int
    user_id: int
    user_request_id: int
    service_name: str
    status_name: str
    date_created: datetime

