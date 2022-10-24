from apps.educational_institutions.models import faculty_list_view, Faculty, speciality_list_view, Course
from apps.educational_institutions.schemas import FacultyOut, FacultyIn, SpecialityListOut, CourseListOut
from apps.users.handlers import get_current_user
from apps.common.db import database

from sqlalchemy import select, insert

from typing import List

from fastapi import Depends, APIRouter

from apps.jsend import JSENDOutSchema


educational_institutions_router = APIRouter()


@educational_institutions_router.get("/{university_id}/faculties/", response_model=JSENDOutSchema[List[FacultyOut]],
                                     tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user=Depends(get_current_user)):
    query = select(faculty_list_view).where(faculty_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got faculty list of the university with id {university_id}"
    }


@educational_institutions_router.post("/{university_id}/faculties/", response_model=JSENDOutSchema[FacultyOut],
                                      tags=["SuperAdmin dashboard"])
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


@educational_institutions_router.get("/{university_id}/speciality/", response_model=JSENDOutSchema[List[SpecialityListOut]],
                                     tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    query = select(speciality_list_view).where(speciality_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got speciality list of the university with id {university_id}"
    }


@educational_institutions_router.get("/courses/", response_model=JSENDOutSchema[List[CourseListOut]],
                                     tags=["Admin dashboard"])
async def read_courses_list(auth=Depends(get_current_user)):
    query = select(Course)
    return {
        "data": await database.fetch_all(query),
        "message": "Got all courses"
    }
