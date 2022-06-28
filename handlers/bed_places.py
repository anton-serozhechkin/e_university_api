from handlers.current_user import get_current_user
from schemas.bed_places import BedPlacesOut
from models.bed_places import bed_places
from db import database

from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/display-bed-places/", response_model=List[BedPlacesOut], tags=["Admin dashboard"])
async def available_bed_places(user = Depends(get_current_user)):
    query = bed_places.select()
    return await database.fetch_all(query)
