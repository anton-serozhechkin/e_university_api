from apps.common.utils import (create_access_token, create_refresh_token, verify_password)
from apps.authorization.models import Role
from apps.users.handlers import get_current_user
from apps.common.exceptions import BackendException
from apps.authorization.schemas import AvailableRolesOut
from apps.common.schemas import JSENDOutSchema
from apps.users.models import User
from apps.users.schemas import AuthOut
from apps.common.db import database

from typing import List
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select


authorization_router = APIRouter()


@authorization_router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut,
                           tags=["Authorization"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = select(User).where(User.login == form_data.username)
    user = await database.fetch_one(query)
    if not user:
        raise BackendException(
            message="Login or password is invalid. Please, try again."
        )

    hashed_pass = user.password

    if not verify_password(form_data.password, hashed_pass):
        raise BackendException(
            message="Email or password is invalid. Please, try again."
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "user_id": user.user_id
    }


@authorization_router.get("/roles/", response_model=JSENDOutSchema[List[AvailableRolesOut]], tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    query = select(Role)
    return {
        "data": await database.fetch_all(query),
        "message": "Got roles"
    }
