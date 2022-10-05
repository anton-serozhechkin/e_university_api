from models.user import user as user_table
from models.user_list_view import user_list_view
from settings import Settings
from db import database
from schemas.user import TokenPayload, UserOut

from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Термін дії токена закінчився",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не вдалося перевірити облікові дані",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    query = user_table.select().where(user_table.c.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача не знайдено",
        )

    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    user = await database.fetch_one(query)

    return user
