from models.user import user as user_table
from models.user_faculty import user_faculty as user_faculty_table
from settings.globals import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from db import database
from schemas.current_user import TokenPayload, UserOut

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
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
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

    user_faculty_query = user_faculty_table.select().where(user_faculty_table.c.user_id == user.user_id)
    user_faculty = await database.fetch_all(user_faculty_query)
    user_faculties_list = []
    for item in user_faculty:
        user_faculties_list.append(item.faculty_id)

    response = UserOut(**user, faculty_id=user_faculties_list)
    return response
