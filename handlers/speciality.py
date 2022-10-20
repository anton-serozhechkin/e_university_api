from models.speciality_list_view import speciality_list_view
from schemas.speciality import SpecialityListOut
from handlers.current_user import get_current_user

from db import database
from typing import List

from fastapi import APIRouter, Depends

from schemas.jsend import JSENDOutSchema


router = APIRouter()


@router.get("/{university_id}/speciality/", response_model=JSENDOutSchema[List[SpecialityListOut]], tags=["Admin dashboard"])
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    query = speciality_list_view.select().where(speciality_list_view.c.university_id == university_id)                                  
    return JSENDOutSchema[List[SpecialityListOut]](
        data=await database.fetch_all(query),
        message=f"Get speciality list of the university with id {university_id}"
    )
