from handlers.current_user import get_current_user
from schemas.role import AvailableRolesOut
from models.role import Role as role_table
from db import database
from sqlalchemy import select
from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/roles/", response_model=List[AvailableRolesOut], tags=["SuperAdmin dashboard"])

# async def available_roles(user = Depends(get_current_user)):
async def available_roles():
    query = select(role_table)
    return await database.fetch_all(query)
