from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.role import AvailableRolesOut
from models.role import Role as role_table
from models.user import User as user
from db import database

from typing import List

from fastapi import Depends, APIRouter

router = APIRouter()


@router.get("/roles/", response_model=List[AvailableRolesOut], tags=["SuperAdmin dashboard"])
async def available_roles(use=Depends(get_current_user)):
    return await database.execute(select(role_table))
