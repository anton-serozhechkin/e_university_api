from sqlalchemy import select, insert

from models.faculty import Faculty
from models.faculty_list_view import faculty_list_view
from schemas.faculty import FacultyOut, FacultyIn
from handlers.current_user import get_current_user
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/{university_id}/faculties/", response_model=JSENDOutSchema[List[FacultyOut]],
            tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user=Depends(get_current_user)):
    query = select(faculty_list_view).where(faculty_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got faculty list of the university with id {university_id}"
    }


@router.post("/{university_id}/faculties/", response_model=JSENDOutSchema[FacultyOut], tags=["SuperAdmin dashboard"])
async def create_faculty(university_id: int, faculty: FacultyIn, user=Depends(get_current_user)):
    query = insert(Faculty).values(name=faculty.name, shortname=faculty.shortname,
                                   main_email=faculty.main_email,
                                   university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        "data": {
            **faculty.dict(),
            "faculty_id": last_record_id
        },
        "message": f"Successfully created faculty with id {last_record_id}"
    }
