from sqlalchemy import select

from models.course import Course
from schemas.course import CourseListOut
from handlers.current_user import get_current_user

from db import database
from typing import List

from fastapi import APIRouter, Depends

from schemas.jsend import JSENDOutSchema


router = APIRouter(tags=["Admin dashboard"])


@router.get("/courses/",
            name="read_courses_list",
            response_model=JSENDOutSchema[List[CourseListOut]],
            summary="Get courses list",
            responses={200: {"description": "Successful get all courses list response"}})
async def read_courses_list(auth=Depends(get_current_user)):
    """
    **Get all courses list.**

    **Auth**: only authenticated user can get courses list.

    **Return**: list of all courses.
    """
    query = select(Course)
    return {
        "data": await database.fetch_all(query),
        "message": "Got all courses"
    }
