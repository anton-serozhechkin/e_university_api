from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.educational_institutions.handlers import edu_institutions_handler
from apps.educational_institutions.schemas import (
    CourseListOut,
    FacultyIn,
    FacultyOut,
    SpecialityListOut,
)

educational_institutions_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@educational_institutions_router.get(
    "/{university_id}/faculties/",
    name="read_faculty_list",
    response_model=JSENDOutSchema[List[FacultyOut]],
    summary="Get list of faculties",
    responses={
        200: {"description": "Successful get list of university faculties response"},
    },  # TODO after input id of non-existent university it returns success,
    tags=["SuperAdmin dashboard"],
)
async def read_faculties(
    request: Request,
    university_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Get list of university faculties**.

    **Path**:
    - **university_id**: integer, required, university id in table

    **Return**:
    - **faculty_id:** id of faculty
    - **name:** faculty name
    - **shortname:** faculty short name
    - **main_email:** main email of faculty
    - **university_id:** id of faculty's university
    - **dean_id:** id of faculty's dean
    - **dean_full_name:** full name of faculty's dean
    """
    return {
        "data": await edu_institutions_handler.read_faculties(
            request=request, university_id=university_id, session=session
        ),
        "message": f"Got faculty list of the university with id {university_id}",
    }


@educational_institutions_router.post(
    "/{university_id}/faculties/",
    name="create_faculty",
    response_model=JSENDOutSchema[FacultyOut],
    summary="Create faculty",
    responses={
        200: {"description": "Successful create faculty in university response"}
    },
    tags=["SuperAdmin dashboard"],
)
async def create_faculty(
    request: Request,
    university_id: int,
    faculty: FacultyIn,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for creating university faculty**.

    **Auth**:
    - only authenticated user can get courses list

    **Path**:
    - **university_id**: path, integer, required, university id in table

    **Input**:
    - **university_id**: integer, university id in table, required
    - **name**: string, full faculty name, required
    - **shortname**: string, short faculty name, required
    - **main_email**: string, faculty main email, not required
    - **dean_id**: integer, id of existing faculty's dean, not required
    - **dean_last_name**: string, last name of faculty's dean, not required
    - **dean_first_name**: string, first name of faculty's dean, not required
    - **dean_middle_name**: string, middle name of faculty's dean, not required

    **Return** faculty list with:
    - **faculty_id**: int, id of created faculty
    - **name**: str, faculty's full name
    - **shortname**: str, faculty's short name
    - **main_email**: str, email of faculty
    - **university_id**: int, id of facultys university
    - **dean_id**: int, id of created or existing faculty's dean
    - **dean_full_name**: dict, full name of created or existing faculty's dean
    """
    response = await edu_institutions_handler.create_faculty(
        request=request, data=faculty, session=session
    )
    return {
        "data": response,
        "message": f"Successfully created faculty with id {response.faculty_id}",
    }  # TODO There is need to add dean to new faculty (change FacultyIn)


@educational_institutions_router.get(
    "/{university_id}/speciality/",
    name="read_speciality_list",
    response_model=JSENDOutSchema[List[SpecialityListOut]],
    summary="Get speciality list",
    responses={
        200: {
            "description": "Successful get all speciality list of university response"
        }
    },
    tags=["Admin dashboard"],
)
async def read_speciality_list(
    request: Request,
    university_id: int,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await edu_institutions_handler.read_speciality_list(
            request=request, university_id=university_id, session=session
        ),
        "message": f"Got speciality list of the university with id {university_id}",
    }


@educational_institutions_router.get(
    "/courses/",
    name="read_courses_list",
    response_model=JSENDOutSchema[List[CourseListOut]],
    summary="Get courses list",
    responses={200: {"description": "Successful get all courses list response"}},
    tags=["Admin dashboard"],
)
async def read_courses_list(
    request: Request,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await edu_institutions_handler.read_courses_list(
            request=request, session=session
        ),
        "message": "Got all courses",
    }
