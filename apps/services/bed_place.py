from apps.hostel.models import BedPlace
from apps.hostel.schemas import BedPlaceOut
from apps.jsend import JSENDOutSchema

from apps.common.db import database

from sqlalchemy import select
from fastapi import Depends, APIRouter

from typing import List

from apps.users.handlers import get_current_user

router = APIRouter()


@router.get("/bed-places/", response_model=JSENDOutSchema[List[BedPlaceOut]], tags=["Admin dashboard"])
async def available_bed_places(user=Depends(get_current_user)):
    query = select(BedPlace)
    return {
        "data": await database.fetch_all(query),
        "message": "Got available bed places list"
    }
