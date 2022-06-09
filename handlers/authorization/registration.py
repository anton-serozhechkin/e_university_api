from models.student import student as student_table
from models.one_time_token import one_time_token
from db import database
import hashlib
import os
from settings.globals import TOKEN_LIFE_TIME
from datetime import date, datetime, timedelta
from components.email_validator import validate_email

from pydantic import BaseModel, validator
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


class RegistrationIn(BaseModel):
    token: str
    email: str
    password: str
    password_re_check: str
    
    @validator('email')
    def email_validator(cls, v):
        try:
            validate_email(v)
        except:
            return JSONResponse(status_code=400, content={"message": "Перевірте правильність вводу електронної пошти"})
    

class Registration(BaseModel):
    message: str



@router.post("/registration/", response_model=Registration)
async def registation(user: RegistrationIn):
    query = one_time_token.select().where(one_time_token.c.token == user.token)
    token_data = await database.fetch_all(query)
    if not token_data:
        return JSONResponse(status_code=404, content={"message": "Для реєстрації користувача, спочатку перейдіть на сторінку перевірки наявності студента в реєстрі"})
    # iteration by result, token expires 
    for token in token_data: 
        expires = token.expires
        student_id = token.student_it
    datetime_utc_now = datetime.utcnow()
    print(datetime_utc_now)
    print(type(expires))
    if datetime_utc_now > expires:
        return JSONResponse(status_code=403, content={"message": "Час на реєстрацію вичерпано, перейдіть на посилання для перевірки студента."})
    
    query = student_table.select().where(student_table.c.student_id == student_id)
    student = await database.fetch_all(query)
    if not student:
        return JSONResponse(status_code=404, content={"message": "Студента не знайдено"})

    #token = hashlib.sha1(os.urandom(128)).hexdigest()
    #expires = datetime.utcnow() + timedelta(seconds=TOKEN_LIFE_TIME)
#
    #query = one_time_token.insert().values(student_id=student_id, token=token,
    #                                       expires=expires).returning(one_time_token.c.token_id)                      
    #last_record_id = await database.execute(query)
    #query = one_time_token.select().where(one_time_token.c.token_id == last_record_id)
    #result = await database.fetch_all(query)
    #for token in result:
    #    response = {'token': token.token, 'student': token.student_id, 'expires': token.expires}
    #return response

