from sqlalchemy import select

from schemas.hostel import HostelListOut
from models.hostel_list_view import hostel_list_view
from db import database
from handlers.current_user import get_current_user

from typing import List

from fastapi import APIRouter, Depends

from schemas.jsend import JSENDOutSchema, JSENDFailOutSchema


router = APIRouter(
    tags=["Admin dashboard"],
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@router.get("/{university_id}/hostels/",
            name="read_university_hostels",
            response_model=JSENDOutSchema[List[HostelListOut]],
            summary="Get university hostels",
            responses={200: {"description": "Successful get all university hostels response"}})
async def read_hostels(university_id: int, user=Depends(get_current_user)):
    query = select(hostel_list_view).where(hostel_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got hostels list of the university with id {university_id}"
    }
