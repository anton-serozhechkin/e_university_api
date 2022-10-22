from sqlalchemy import select, insert

from models.student import Student
from models.one_time_token import OneTimeToken
from db import database
from schemas.student import StudentCheckExistanceIn, StudentCheckExistanceOut
from settings import Settings

from datetime import datetime, timedelta
import hashlib
import os

from fastapi import APIRouter, status as http_status

from schemas.jsend import JSENDOutSchema, JSENDErrorOutSchema, JSENDFailOutSchema
from components.exceptions import BackendException

router = APIRouter(
    responses={422: {"model": JSENDErrorOutSchema, "description": "ValidationError"},
               404: {"model": JSENDFailOutSchema, "description": "Invalid input data"}}
)


@router.post("/check-student-existance",
             name="post_student_existence",
             response_model=JSENDOutSchema[StudentCheckExistanceOut],
             summary="Check user existence",
             responses={200: {"description": "Check user existence"}},
             tags=["Authorization"])  # TODO spelling mistake, there is need to check path in other modules
async def check_student(student: StudentCheckExistanceIn):

    query = select(Student).where(Student.full_name == student.full_name,
                                  Student.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        raise BackendException(
            message="Student data was not found. Please, try again.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)

    query = insert(OneTimeToken).values(student_id=student_id, token=token,
                                        expires=expires).returning(OneTimeToken.token_id)
    last_record_id = await database.execute(query)

    query = select(OneTimeToken).where(OneTimeToken.token_id == last_record_id)
    result = await database.fetch_one(query)

    return {
        "data": {
            'token': result.token,
            'student': result.student_id,
            'expires': result.expires
        },
        "message": f"Get information of student with id {result.student_id}"
    }
