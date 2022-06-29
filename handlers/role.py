from handlers.current_user import get_current_user
from schemas.role import AvailableRolesOut
from models.role import role as role_table 
from db import database

from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/available-role/", response_model=List[AvailableRolesOut], tags=["SuperAdmin dashboard"])
async def available_roles(user = Depends(get_current_user)):
    query = role_table.select()
    return await database.fetch_all(query)
    