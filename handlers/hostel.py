from schemas.hostel import HostelListOut
from models.hostel_list_view import hostel_list_view
from db import database

from typing import List

from fastapi import APIRouter

router = APIRouter()

@router.get("/{university_id}/hostels/", response_model=List[HostelListOut], tags=["SuperAdmin dashboard"])
async def available_bed_places(university_id: int):
    query = hostel_list_view.select().where(hostel_list_view.c.university_id == university_id)
    return await database.fetch_all(query)