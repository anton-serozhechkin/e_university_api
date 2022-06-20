from datetime import datetime

from pydantic import BaseModel


class TokenPayload(BaseModel):
    exp: int
    sub: str


class UserOut(BaseModel):
    user_id: int
    login: str
    last_visit: datetime = None
    email: str
    is_active: bool
    role_id: int
    faculty_id: list


class UserIn(TokenPayload):
    user_id: int
