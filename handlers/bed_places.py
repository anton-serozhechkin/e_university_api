from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.bed_places import BedPlacesOut
from models.bed_places import BedPlaces
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter(tags=["Admin dashboard"])


@router.get("/bed-places/",
            name="get_bed_places",
            response_model=JSENDOutSchema[List[BedPlacesOut]],
            summary="Get bed places list",
            responses={200: {"description": "Successful get list of available bed places response"}})
async def available_bed_places(user=Depends(get_current_user)):
    """
    **Get available bed places list.**

    **Auth**: only authenticated user can get courses list

    **Return**: list of available bed places.
    """
    query = select(BedPlaces)
    return {
        "data": await database.fetch_all(query),
        "message": "Got available bed places list"
    }
