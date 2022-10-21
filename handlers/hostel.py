from sqlalchemy import select

from schemas.hostel import HostelListOut
from models.hostel_list_view import hostel_list_view
from db import database
from handlers.current_user import get_current_user

from typing import List

from fastapi import APIRouter, Depends

from schemas.jsend import JSENDOutSchema


router = APIRouter()


@router.get("/{university_id}/hostels/", response_model=JSENDOutSchema[List[HostelListOut]], tags=["Admin dashboard"])
async def read_hostels(university_id: int, user=Depends(get_current_user)):
    query = select(hostel_list_view).where(hostel_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got hostels list of the university with id {university_id}"
    }
