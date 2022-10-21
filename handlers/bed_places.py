from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.bed_places import BedPlacesOut
from models.bed_places import BedPlaces
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/bed-places/", response_model=JSENDOutSchema[List[BedPlacesOut]], tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    query = select(BedPlaces)
    return {
        "data": await database.fetch_all(query),
        "message": "Got available bed places list"
    }
