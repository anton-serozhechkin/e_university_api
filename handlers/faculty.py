from models.faculty import faculty as faculty_table
from schemas.faculty import FacultyOut, FacultyIn
from handlers.current_user import get_current_user
from db import database

from typing import List

from fastapi import Depends, APIRouter 


router = APIRouter()


@router.get("/{university_id}/faculties/", response_model=List[FacultyOut])
async def read_faculties(university_id: int, user = Depends(get_current_user)):
    query = faculty_table.select().where(faculty_table.c.university_id == university_id)
    return await database.fetch_all(query)


@router.post("/{university_id}/faculties/", response_model=FacultyOut)
async def create_faculty(faculty: FacultyIn, user = Depends(get_current_user)):
    query = faculty_table.insert().values(name=faculty.name, shortname=faculty.shortname, 
                                    main_email=faculty.main_email, 
                                    university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        **faculty.dict(), 
        "faculty_id": last_record_id
    }
