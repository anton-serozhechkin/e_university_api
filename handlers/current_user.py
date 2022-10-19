from models.user import user as user_table
from models.user_list_view import user_list_view
from settings import Settings
from db import database
from schemas.user import TokenPayload, UserOut

from datetime import datetime

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from components.exceptions import BackendException


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)       # TODO syntax error


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise BackendException(
                message="Token data has expired",
                code=status.HTTP_401_UNAUTHORIZED
            )       # TODO didn't include headers, did it need?

    except(jwt.JWTError, ValidationError):
        raise BackendException(
            message="Credential verification failed",
            code=status.HTTP_403_FORBIDDEN
        )       # TODO didn't include headers, did it need?
        
    query = user_table.select().where(user_table.c.email == token_data.sub)
    user = await database.fetch_one(query)

    if user is None:
        raise BackendException(
            message="User not found",
            code=status.HTTP_404_NOT_FOUND
        )

    query = user_list_view.select(user_list_view.c.user_id == user.user_id)
    user = await database.fetch_one(query)

    return user
