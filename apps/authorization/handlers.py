from apps.authorization.services import (create_access_token, create_refresh_token, verify_password)
from apps.authorization.models import Role
from apps.common.exceptions import BackendException
from apps.users.models import User
from apps.common.db import database

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select


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


async def available_roles():
    query = select(Role)
    return await database.fetch_all(query)
