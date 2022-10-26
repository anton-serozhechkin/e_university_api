from apps.users.handlers import get_current_user
from apps.authorization.schemas import AvailableRolesOut
from apps.common.schemas import JSENDOutSchema
from apps.users.schemas import AuthOut
from apps.authorization import handlers

from typing import List
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


authorization_router = APIRouter()


@authorization_router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut,
                           tags=["Authorization"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await handlers.login(form_data)


@authorization_router.get("/roles/", response_model=JSENDOutSchema[List[AvailableRolesOut]], tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    return {
        "data": await handlers.available_roles(),
        "message": "Got roles"
    }
