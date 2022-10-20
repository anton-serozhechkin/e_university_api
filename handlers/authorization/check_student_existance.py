from models.student import student as student_table
from models.one_time_token import one_time_token
from db import database
from schemas.student import StudentCheckExistanceIn, StudentCheckExistanceOut
from settings import Settings

from datetime import datetime, timedelta
import hashlib
import os

from fastapi import APIRouter, status as http_status

from schemas.jsend import JSENDOutSchema
from components.exceptions import BackendException

router = APIRouter()


@router.post("/check-student-existance", response_model=JSENDOutSchema[StudentCheckExistanceOut],
             tags=["Authorization"])  # TODO syntax error, there is need to check path in other modules
async def check_student(student: StudentCheckExistanceIn):
    query = student_table.select().where(student_table.c.full_name == student.full_name,
                                         student_table.c.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        raise BackendException(
            message="Student data was not found. Please, try again.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)

    query = one_time_token.insert().values(student_id=student_id, token=token,
                                           expires=expires).returning(one_time_token.c.token_id)
    last_record_id = await database.execute(query)

    query = one_time_token.select().where(one_time_token.c.token_id == last_record_id)
    result = await database.fetch_one(query)

    response = {
        'token': result.token,
        'student': result.student_id,
        'expires': result.expires
    }

    return JSENDOutSchema[StudentCheckExistanceOut](
        data=response,
        message=f"Get information of student with id {result.student_id}"
    )
