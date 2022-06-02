from typing import List

from db import database
from pydantic import BaseModel
from models.faculty import faculty as faculty_table
from fastapi import APIRouter 


router = APIRouter()


class FacultyIn(BaseModel):
    name: str
    shortname: str
    hostel_email: str
    main_email: str


class Faculty(BaseModel):
    faculty_id: int
    name: str
    shortname: str
    hostel_email: str
    main_email: str


@router.get("/faculties/", response_model=List[Faculty])
async def read_faculties():
    query = faculty_table.select()
    return await database.fetch_all(query)


@router.post("/faculties/", response_model=None)
async def create_faculty(faculty: FacultyIn):
    query = faculty_table.insert().values(name=faculty.name, shortname=faculty.shortname, 
                                    hostel_email=faculty.hostel_email, 
                                    main_email=faculty.main_email)
    last_record_id = await database.execute(query)
    return {**faculty.dict(), "faculty_id": last_record_id}
