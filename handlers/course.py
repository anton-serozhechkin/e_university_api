from sqlalchemy import select

from models.course import Course as course
from schemas.course import CourseListOut
from handlers.current_user import get_current_user

from db import database
from typing import List

from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/courses/", response_model=List[CourseListOut], tags=["Admin dashboard"])
async def read_courses_list(auth=Depends(get_current_user)):
    query = select(course)
    return await database.fetch_all(query)
