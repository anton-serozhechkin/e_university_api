from sqlalchemy import select
from sqlalchemy.testing.pickleable import User

from apps.authorization.schemas import AvailableRolesOut
from apps.core.db import database
from typing import List

from fastapi import Depends, APIRouter
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


from apps.components.utils import (create_access_token, create_refresh_token, verify_password)

from apps.authorization.models import Role
from apps.users.handlers import get_current_user

router = APIRouter()


@router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut,
             tags=["Authorization"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = select(User).where(User.login == form_data.username)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некоректний логін або пароль. Будь ласка, спробуйте ще раз."
        )

    hashed_pass = user.password

    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невірна електронна адреса або пароль."
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "user_id": user.user_id
    }


@router.get("/roles/", response_model=List[AvailableRolesOut], tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    query = select(Role)
    return await database.fetch_all(query)
