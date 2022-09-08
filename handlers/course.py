from models.course import course
from schemas.course import CourseListOut

from db import database
from typing import List

from fastapi import APIRouter


router = APIRouter()


@router.get("/courses/", response_model=List[CourseListOut], tags=["Admin dashboard"])
async def read_courses_list():
    query = course.select()
    return await database.fetch_all(query)
