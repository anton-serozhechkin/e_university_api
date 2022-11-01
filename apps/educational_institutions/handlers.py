from apps.educational_institutions.models import faculty_list_view, Faculty, speciality_list_view, Course
from apps.educational_institutions.schemas import FacultyOut, FacultyIn, SpecialityListOut, CourseListOut
from apps.users.handlers import get_current_user
from apps.common.db import database

from sqlalchemy import select, insert

from typing import List

from fastapi import Depends, APIRouter, status as http_status

from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema


educational_institutions_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@educational_institutions_router.get("/{university_id}/faculties/",
                                     name="read_faculty_list",
                                     response_model=JSENDOutSchema[List[FacultyOut]],
                                     summary="Get faculty list",
                                     responses={
                                         200: {"description": "Successful get faculty list of university response"},
                                     },  # TODO after input id of non-existent university it returns success,
                                     tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user=Depends(get_current_user)):
    """
        **Get list of university faculties**

        **Path**:
        - **university_id**: integer, required, university id in table

        **Return**: list of all university faculties with info: faculty id in table, name and shortname,
        email, university id in table, decan full name
    """
    query = select(faculty_list_view).where(faculty_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got faculty list of the university with id {university_id}"
    }


@educational_institutions_router.post("/{university_id}/faculties/",
                                      name="create_faculty",
                                      response_model=JSENDOutSchema[FacultyOut],
                                      summary="Create faculty",
                                      responses={
                                          200: {"description": "Successful create faculty in university response"}
                                      },
                                      tags=["SuperAdmin dashboard"])
async def create_faculty(university_id: int, faculty: FacultyIn, user=Depends(get_current_user)):
    """
        **Create faculty in university**

        **Auth**: only authenticated user can get courses list.

        **Path**:

        - **university_id**: path, integer, required, university id in table

        **Input** required

        - **university_id**: integer, university id in table
        - **name**: string, full faculty name
        - **shortname**: string, short faculty name
        - **main_email**: string, faculty main email

        **Return**: list of all university faculties with info: faculty id in table, name and shortname,
        email, university id in table, decan full name
    """
    query = insert(Faculty).values(name=faculty.name, shortname=faculty.shortname,
                                   main_email=faculty.main_email,
                                   university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        "data": {
            **faculty.dict(),
            "faculty_id": last_record_id
        },
        "message": f"Successfully created faculty with id {last_record_id}",
        "code": http_status.HTTP_201_CREATED
    }


@educational_institutions_router.get("/{university_id}/speciality/",
                                     name="read_speciality_list",
                                     response_model=JSENDOutSchema[List[SpecialityListOut]],
                                     summary="Get speciality list",
                                     responses={200: {
                                         "description": "Successful get all speciality list of university response"}
                                     },
                                     tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    query = select(speciality_list_view).where(speciality_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got speciality list of the university with id {university_id}"
    }


@educational_institutions_router.get("/courses/",
                                     name="read_courses_list",
                                     response_model=JSENDOutSchema[List[CourseListOut]],
                                     summary="Get courses list",
                                     responses={200: {"description": "Successful get all courses list response"}},
                                     tags=["Admin dashboard"])
async def read_courses_list(auth=Depends(get_current_user)):
    query = select(Course)
    return {
        "data": await database.fetch_all(query),
        "message": "Got all courses"
    }
