from handlers.current_user import get_current_user
from schemas.bed_place import
from models.bed_place import bed_place
from db import database

from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/bed-place/", response_model=List[BedPlaceOut], tags=["Admin dashboard"])
async def available_bed_places():# user = Depends(get_current_user)):
    query = bed_place.select()
    return await database.fetch_all(query)
