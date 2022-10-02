from apps.hostel.schemas import HostelListOut, BedPlacesOut
from models.hostel_list_view import hostel_list_view
from apps.hostel.models import bed_places
from db import database
from handlers.current_user import get_current_user

from typing import List

from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/{university_id}/hostels/", response_model=List[HostelListOut], tags=["Admin dashboard"])
async def read_hostels(university_id: int, user = Depends(get_current_user)):
    query = hostel_list_view.select().where(hostel_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


@router.get("/bed-places/", response_model=List[BedPlacesOut], tags=["Admin dashboard"])
async def available_bed_places(user = Depends(get_current_user)):
    query = bed_places.select()
    return await database.fetch_all(query)
