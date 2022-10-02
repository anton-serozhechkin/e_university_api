from apps.educational_instuctions.models import faculty as faculty_table
from apps.educational_instuctions.models import course
from models.faculty_list_view import faculty_list_view
from models.speciality_list_view import speciality_list_view
from apps.educational_instuctions.schemas import FacultyOut, FacultyIn, SpecialityListOut, CourseListOut
from handlers.current_user import get_current_user
from db import database

from typing import List

from fastapi import Depends, APIRouter 


router = APIRouter()


@router.get("/{university_id}/faculties/", response_model=List[FacultyOut], tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user = Depends(get_current_user)):
    query = faculty_list_view.select().where(faculty_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


@router.post("/{university_id}/faculties/", response_model=FacultyOut, tags=["SuperAdmin dashboard"])
async def create_faculty(university_id: int, faculty: FacultyIn, user = Depends(get_current_user)):
    query = faculty_table.insert().values(name=faculty.name, shortname=faculty.shortname, 
                                    main_email=faculty.main_email, 
                                    university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        **faculty.dict(), 
        "faculty_id": last_record_id
    }


@router.get("/{university_id}/speciality/", response_model=List[SpecialityListOut], tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth = Depends(get_current_user)):
    query = speciality_list_view.select().where(speciality_list_view.c.university_id == university_id)                                  
    return await database.fetch_all(query)


@router.get("/courses/", response_model=List[CourseListOut], tags=["Admin dashboard"])
async def read_courses_list(auth = Depends(get_current_user)):
    query = course.select()
    return await database.fetch_all(query)
