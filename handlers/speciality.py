from sqlalchemy import select

from models.speciality_list_view import speciality_list_view
from schemas.speciality import SpecialityListOut
from handlers.current_user import get_current_user

from db import database
from typing import List

from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/{university_id}/speciality/", response_model=List[SpecialityListOut], tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth = Depends(get_current_user)):
    query = select(speciality_list_view).where(speciality_list_view.c.university_id == university_id)
    return await database.execute(query)
