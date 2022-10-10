from sqlalchemy import select, insert

from models.faculty import Faculty as faculty_table
from models.faculty_list_view import faculty_list_view
from schemas.faculty import FacultyOut, FacultyIn
from handlers.current_user import get_current_user
from db import database

from typing import List

from fastapi import Depends, APIRouter 


router = APIRouter()


@router.get("/{university_id}/faculties/", response_model=List[FacultyOut], tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user=Depends(get_current_user)):
    query = select(faculty_list_view).where(faculty_list_view.c.university_id == university_id)
    return await database.execute(query)


@router.post("/{university_id}/faculties/", response_model=FacultyOut, tags=["SuperAdmin dashboard"])
async def create_faculty(university_id: int, faculty: FacultyIn, user=Depends(get_current_user)):
    query = insert(faculty_table).values(name=faculty.name, shortname=faculty.shortname,
                                         main_email=faculty.main_email,
                                         university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        **faculty.dict(), 
        "faculty_id": last_record_id
    }
