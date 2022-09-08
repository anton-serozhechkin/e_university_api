from models.course_list_view import course_list_view
from schemas.course import CourseListOut

from db import database

from typing import List

from fastapi import APIRouter

router = APIRouter()

@router.get("/courses/", response_model=List[CourseListOut], tags=["Admin dashboard"])
async def courses_list():
    query = course_list_view.select()
    return await database.fetch_all(query)