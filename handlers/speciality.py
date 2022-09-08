from models.speciality_list_view import speciality_list_view
from schemas.speciality import SpecialityListOut

from db import database
from typing import List

from fastapi import APIRouter


router = APIRouter()


@router.get("/{university_id}/speciality/", response_model=List[SpecialityListOut], tags=["Admin dashboard"])
async def read_speciality_list(university_id: int):
    query = speciality_list_view.select().where(speciality_list_view.c.university_id == university_id)                                  
    return await database.fetch_all(query)
