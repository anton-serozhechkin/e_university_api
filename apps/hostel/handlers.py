from apps.core.db import database
from apps.hostel.models import BedPlaces, hostel_list_view
from apps.hostel.schemas import HostelListOut, BedPlacesOut
from apps.users.handlers import get_current_user

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select

router = APIRouter()


@router.get("/{university_id}/hostels/", response_model=List[HostelListOut], tags=["Admin dashboard"])
async def read_hostels(university_id: int, user=Depends(get_current_user)):
    query = select(hostel_list_view).where(hostel_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


@router.get("/bed-places/", response_model=List[BedPlacesOut], tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    query = select(BedPlaces)
    return await database.fetch_all(query)
