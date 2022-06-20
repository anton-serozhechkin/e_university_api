from components.utils import (
    create_access_token,
    create_refresh_token,
    verify_password
)
from models.user import user as user_table
from db import database

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import AuthOut


router = APIRouter()


@router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = user_table.select().where(user_table.c.login == form_data.username)
    user = await database.fetch_all(query)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некоректний логін або пароль. Будь ласка, спробуйте ще раз."
        )

    hashed_pass = user[0]['password']

    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невірна електронна адреса або пароль."
        )
    
    return {
        "access_token": create_access_token(user[0]['email']),
        "refresh_token": create_refresh_token(user[0]['email']),
        "user_id": user[0]['user_id']
    }
