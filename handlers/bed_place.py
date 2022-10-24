from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.bed_place import BedPlaceOut
from models.bed_place import BedPlace
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter(tags=["Admin dashboard"])


@router.get("/bed-places/",
            name="read_bed_places",
            response_model=JSENDOutSchema[List[BedPlaceOut]],
            summary="Get bed places list",
            responses={200: {"description": "Successful get list of available bed places response"}})
async def available_bed_places(user=Depends(get_current_user)):
    query = select(BedPlace)
    return {
        "data": await database.fetch_all(query),
        "message": "Got available bed places list"
    }
