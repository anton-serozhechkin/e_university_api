from datetime import datetime

from pydantic import BaseModel


class StudentCheckExistanceIn(BaseModel):
    full_name: str
    telephone_number: str


class StudentCheckExistanceOut(BaseModel):
    student: int
    token: str
    expires: datetime
