from components.utils import (
    create_access_token,
    create_refresh_token,
    verify_password
)
from apps.users.models import user as user_table
from db import database

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from apps.users.schemas import AuthOut


router = APIRouter()


@router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut, tags=["Authorization"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = user_table.select().where(user_table.c.login == form_data.username)
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
