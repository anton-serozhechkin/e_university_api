from apps.hostel.schemas import HostelListOut, BedPlaceOut
from apps.users.handlers import get_current_user
from apps.hostel import handlers

from typing import List

from fastapi import APIRouter, Depends
from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema


hostel_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@hostel_router.get("/{university_id}/hostels/",
                   name="read_university_hostels",
                   response_model=JSENDOutSchema[List[HostelListOut]],
                   summary="Get university hostels",
                   responses={
                       200: {"description": "Successful get all university hostels response"},
                       422: {"model": JSENDFailOutSchema, "description": "ValidationError"}
                   },
                   tags=["Admin dashboard"])
async def read_hostels(university_id: int, user=Depends(get_current_user)):
    return {
        "data": await handlers.read_hostels(university_id),
        "message": f"Got hostels list of the university with id {university_id}"
    }


@hostel_router.get("/bed-places/",
                   name="read_bed_places",
                   response_model=JSENDOutSchema[List[BedPlaceOut]],
                   summary="Get bed places list",
                   responses={200: {"description": "Successful get list of available bed places response"}},
                   tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    return {
        "data": await handlers.read_available_bed_places(),
        "message": "Got available bed places list"
    }
