from handlers.current_user import get_current_user
from schemas.role import AvailableRoleOut
from models.role import role as role_table 
from db import database

from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/dispay_role/", response_model=List[AvailableRoleOut], tags=["Admin dashboard"])
async def available_role(user = Depends(get_current_user)):
    query = role_table.select()
    return await database.fetch_all(query)
    