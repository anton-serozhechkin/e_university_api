from models.faculty import faculty as faculty_table
from db import database

from typing import List
import re

from pydantic import BaseModel, validator
from fastapi import APIRouter 


router = APIRouter()


class FacultyIn(BaseModel):
    university_id: int
    name: str
    shortname: str
    main_email: str

    @validator('main_email')
    def validate_email(cls, v):
        """
        The method is using for email validation. Only letters (a-z), numbers (0-9) and periods (.) are allowed
        :return: True or not None string
        """
        specials = '!#$%&\'*+-/=?^_`{|?.'
        specials = re.escape(specials)
        regex = re.compile('^(?![' + specials + '])'
                           '(?!.*[' + specials + ']{2})'
                           '(?!.*[' + specials + ']$)'
                           '[A-Za-z0-9' + specials + ']+(?<!['+ specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
        message = False

        if not v:
            message = "Електронний адрес не може бути порожнім"

        elif not re.fullmatch(regex, v):
            message = f"Невірний формат адресу електронної пошти: {v}."

        if message:
            raise ValueError(message)

        return v
    

class Faculty(BaseModel):
    faculty_id: int
    name: str
    shortname: str
    main_email: str
    university_id: int


@router.get("/faculties/", response_model=List[Faculty])
async def read_faculties():
    query = faculty_table.select()
    return await database.fetch_all(query)


@router.post("/faculties/", response_model=Faculty)
async def create_faculty(faculty: FacultyIn):
    query = faculty_table.insert().values(name=faculty.name, shortname=faculty.shortname, 
                                    main_email=faculty.main_email, 
                                    university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        **faculty.dict(), 
        "faculty_id": last_record_id
    }
