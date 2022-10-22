from sqlalchemy import select

from models.speciality_list_view import speciality_list_view
from schemas.speciality import SpecialityListOut
from handlers.current_user import get_current_user

from db import database
from typing import List

from fastapi import APIRouter, Depends

from schemas.jsend import JSENDOutSchema, JSENDErrorOutSchema


router = APIRouter(
    tags=["Admin dashboard"],
    responses={422: {"model": JSENDErrorOutSchema, "description": "ValidationError"}}
)


@router.get("/{university_id}/speciality/",
            name="get_speciality_list",
            response_model=JSENDOutSchema[List[SpecialityListOut]],
            summary="Get speciality list",
            responses={200: {"description": "Get all speciality list of university"}})
async def read_speciality_list(university_id: int, auth=Depends(get_current_user)):
    query = select(speciality_list_view).where(speciality_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got speciality list of the university with id {university_id}"
    }
