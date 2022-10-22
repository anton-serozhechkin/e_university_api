from sqlalchemy import select, insert

from models.student import Student
from models.one_time_token import OneTimeToken
from db import database
from schemas.student import StudentCheckExistanceIn, StudentCheckExistanceOut
from settings import Settings

from datetime import datetime, timedelta
import hashlib
import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("/check-student-existance", response_model=StudentCheckExistanceOut, tags=["Authorization"])
async def check_student(student: StudentCheckExistanceIn):

    query = select(Student).where(Student.full_name == student.full_name,
                                  Student.telephone_number == student.telephone_number)
    result = await database.fetch_one(query)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Дані про студента не знайдено. " \
                                                                "Будь ласка, спробуйте ще раз."})

    student_id = result.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=Settings.TOKEN_LIFE_TIME)

    query = insert(OneTimeToken).values(student_id=student_id, token=token,
                                        expires=expires).returning(OneTimeToken.token_id)
    last_record_id = await database.execute(query)

    query = select(OneTimeToken).where(OneTimeToken.token_id == last_record_id)
    result = await database.fetch_one(query)

    response = {
                'token': result.token,
                'student': result.student_id, 
                'expires': result.expires
    }

    return response
