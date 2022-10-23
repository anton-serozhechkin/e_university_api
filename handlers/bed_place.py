from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.bed_place import BedPlaceOut
from models.bed_place import BedPlace
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/bed-places/", response_model=JSENDOutSchema[List[BedPlaceOut]], tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    query = select(BedPlace)
    return {
        "data": await database.fetch_all(query),
        "message": "Got available bed places list"
    }
