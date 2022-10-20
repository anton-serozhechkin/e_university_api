from models.user import User
from db import database
from components.utils import (create_access_token, create_refresh_token, verify_password)
from schemas.user import AuthOut

from sqlalchemy import select
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from components.exceptions import BackendException

router = APIRouter()


@router.post('/login', summary="Створення доступу та оновлення токена користувача", response_model=AuthOut, tags=["Authorization"])
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
