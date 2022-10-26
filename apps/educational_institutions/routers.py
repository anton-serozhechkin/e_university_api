from apps.educational_institutions.schemas import FacultyOut, FacultyIn, SpecialityListOut, CourseListOut
from apps.users.handlers import get_current_user
from apps.educational_institutions import handlers


from typing import List

from fastapi import Depends, APIRouter

from apps.common.schemas import JSENDOutSchema


educational_institutions_router = APIRouter()


@educational_institutions_router.get("/{university_id}/faculties/", response_model=JSENDOutSchema[List[FacultyOut]],
                                     tags=["SuperAdmin dashboard"])
async def read_faculties(university_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.read_faculties(university_id),
        "message": f"Got faculty list of the university with id {university_id}"
    }


@educational_institutions_router.post("/{university_id}/faculties/", response_model=JSENDOutSchema[FacultyOut],
                                      tags=["SuperAdmin dashboard"])
async def create_faculty(university_id: int, faculty: FacultyIn, user=Depends(get_current_user)):
    response = handlers.create_faculty(faculty)
    return {
        "data": response,
        "message": f"Successfully created faculty with id {response['faculty_id']}"
    }


@educational_institutions_router.get("/{university_id}/speciality/", response_model=JSENDOutSchema[List[SpecialityListOut]],
                                     tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    return {
        "data": handlers.read_speciality_list(university_id),
        "message": f"Got speciality list of the university with id {university_id}"
    }


@educational_institutions_router.get("/courses/", response_model=JSENDOutSchema[List[CourseListOut]],
                                     tags=["Admin dashboard"])
async def read_courses_list(auth=Depends(get_current_user)):
    return {
        "data": handlers.read_courses_list(),
        "message": "Got all courses"
    }
