from apps.hostel.schemas import HostelListOut, BedPlaceOut
from apps.users.handlers import get_current_user
from apps.hostel import handlers

from typing import List

from fastapi import APIRouter, Depends
from apps.common.schemas import JSENDOutSchema


hostel_router = APIRouter()


@hostel_router.get("/{university_id}/hostels/", response_model=JSENDOutSchema[List[HostelListOut]], tags=["Admin dashboard"])
async def read_hostels(university_id: int, user=Depends(get_current_user)):
    return {
        "data": handlers.get_hostels(university_id),
        "message": f"Got hostels list of the university with id {university_id}"
    }


@hostel_router.get("/bed-places/", response_model=JSENDOutSchema[List[BedPlaceOut]], tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    return {
        "data": handlers.get_available_bed_places(),
        "message": "Got available bed places list"
    }
