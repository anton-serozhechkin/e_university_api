from apps.educational_institutions.schemas import FacultyOut, FacultyIn, SpecialityListOut, CourseListOut
from apps.users.handlers import get_current_user
from apps.educational_institutions import handlers


from typing import List

from fastapi import Depends, APIRouter

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
    return {
        "data": await handlers.read_faculties(university_id),
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
    response = await handlers.create_faculty(faculty)
    return {
        "data": response,
        "message": f"Successfully created faculty with id {response['faculty_id']}"
    }   # TODO There is need to add decan to new faculty (change FacultyIn)


@educational_institutions_router.get("/{university_id}/speciality/",
                                     name="read_speciality_list",
                                     response_model=JSENDOutSchema[List[SpecialityListOut]],
                                     summary="Get speciality list",
                                     responses={200: {
                                         "description": "Successful get all speciality list of university response"}
                                     },
                                     tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    return {
        "data": await handlers.read_speciality_list(university_id),
        "message": f"Got speciality list of the university with id {university_id}"
    }


@educational_institutions_router.get("/courses/",
                                     name="read_courses_list",
                                     response_model=JSENDOutSchema[List[CourseListOut]],
                                     summary="Get courses list",
                                     responses={200: {"description": "Successful get all courses list response"}},
                                     tags=["Admin dashboard"])
async def read_courses_list(auth=Depends(get_current_user)):
    return {
        "data": await handlers.read_courses_list(),
        "message": "Got all courses"
    }
