from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.educational_institutions.handlers import edu_institutions_handler
from apps.educational_institutions.schemas import FacultyIn, FacultyOut, CourseListOut, SpecialityListOut
from apps.users.schemas import UserOut

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


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
async def read_faculties(request: Request,
                         university_id: int,
                         user: UserOut = Depends(get_current_user),
                         session: AsyncSession = Depends(get_async_session)):
    """
        **Get list of university faculties**

        **Path**:
        - **university_id**: integer, required, university id in table

        **Return**: list of all university faculties with info: faculty id in table, name and shortname,
        email, university id in table, dean full name
    """
    return {
        "data": await edu_institutions_handler.read_faculties(
            request=request,
            university_id=university_id,
            session=session
        ),
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
async def create_faculty(
        request: Request,
        university_id: int,
        faculty: FacultyIn,
        user: UserOut = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
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
        email, university id in table, dean full name
    """
    response = await edu_institutions_handler.create_faculty(
        request=request,
        data=faculty,
        session=session
        )
    return {
        "data": response,
        "message": f"Successfully created faculty with id {response.dict()['faculty_id']}"
    }   # TODO There is need to add dean to new faculty (change FacultyIn)


@educational_institutions_router.get("/{university_id}/speciality/",
                                     name="read_speciality_list",
                                     response_model=JSENDOutSchema[List[SpecialityListOut]],
                                     summary="Get speciality list",
                                     responses={200: {
                                         "description": "Successful get all speciality list of university response"}
                                     },
                                     tags=["Admin dashboard"])
async def read_speciality_list(
        request: Request,
        university_id: int,
        auth: UserOut = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return {
        "data": await edu_institutions_handler.read_speciality_list(
            request=request,
            university_id=university_id,
            session=session
        ),
        "message": f"Got speciality list of the university with id {university_id}"
    }


@educational_institutions_router.get("/courses/",
                                     name="read_courses_list",
                                     response_model=JSENDOutSchema[List[CourseListOut]],
                                     summary="Get courses list",
                                     responses={200: {"description": "Successful get all courses list response"}},
                                     tags=["Admin dashboard"])
async def read_courses_list(
        request: Request,
        auth: UserOut = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return {
        "data": await edu_institutions_handler.read_courses_list(
            request=request,
            session=session
        ),
        "message": "Got all courses"
    }
