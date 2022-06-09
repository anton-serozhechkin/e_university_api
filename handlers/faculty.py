from models.faculty import faculty as faculty_table
from db import database

from typing import List

from pydantic import BaseModel
from fastapi import APIRouter 


router = APIRouter()


class FacultyIn(BaseModel):
    name: str
    shortname: str
    main_email: str
    


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


@router.post("/faculties/", response_model=None)
async def create_faculty(faculty: FacultyIn):
    query = faculty_table.insert().values(name=faculty.name, shortname=faculty.shortname, 
                                    main_email=faculty.main_email, university_id=1)
    last_record_id = await database.execute(query)
    return {**faculty.dict(), "faculty_id": last_record_id}
