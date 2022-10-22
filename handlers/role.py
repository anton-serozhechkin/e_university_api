from sqlalchemy import select

from handlers.current_user import get_current_user
from schemas.role import AvailableRolesOut
from models.role import Role
from db import database

from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/roles/", response_model=JSENDOutSchema[List[AvailableRolesOut]], tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    query = select(Role)
    return {
        "data": await database.fetch_all(query),
        "message": "Got roles"
    }
