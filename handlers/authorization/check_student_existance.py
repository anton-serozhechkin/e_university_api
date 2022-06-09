from models.student import student as student_table
from models.one_time_token import one_time_token
from db import database
import hashlib
import os
from settings.globals import TOKEN_LIFE_TIME
from datetime import datetime, timedelta


from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


class StudentIn(BaseModel):
    full_name: str
    telephone_number: str
    

class Student(BaseModel):
    student: int
    token: str



@router.post("/check-student-existance/", response_model=None)
async def create_faculty(student: StudentIn):
    query = student_table.select().where(student_table.c.full_name == student.full_name, student_table.c.telephone_number == student.telephone_number)
    result = await database.fetch_all(query)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Дані про студента не знайдено. Спробуйте ще раз."})

    for student in result: 
        student_id = student.student_id

    token = hashlib.sha1(os.urandom(128)).hexdigest()
    expires = datetime.utcnow() + timedelta(seconds=TOKEN_LIFE_TIME)

    query = one_time_token.insert().values(student_id=student_id, token=token,
                                           expires=expires).returning(one_time_token.c.token_id)                      
    last_record_id = await database.execute(query)
    query = one_time_token.select().where(one_time_token.c.token_id == last_record_id)
    result = await database.fetch_all(query)
    for token in result:
        response = {'token': token.token, 'student': token.student_id, 'expires': token.expires}
    return response

