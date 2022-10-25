from apps.common.utils import (create_access_token, create_refresh_token, verify_password)
from apps.authorization.models import Role
from apps.users.handlers import get_current_user
from apps.common.exceptions import BackendException
from apps.authorization.schemas import AvailableRolesOut
from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema
from apps.users.models import User
from apps.users.schemas import AuthOut
from apps.common.db import database

from typing import List
from fastapi import Depends, APIRouter, status as http_status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select


authorization_router = APIRouter()


@authorization_router.post('/login',
                           name="login",
                           response_model=AuthOut,
                           summary="Create access and refresh user token",
                           responses={
                               200: {"description": "Login and refresh user token"},
                               422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
                               401: {"model": JSENDFailOutSchema, "description": "Not authorized response"}
                           },
                           tags=["Authorization"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        **Login user**

        **Input**:
        - **username**: login, which consists of name and random number; required
        - **password**: password to this login name; required

        **Return**: access and refresh tokens for authentication, user id
    """
    query = select(User).where(User.login == form_data.username)
    user = await database.fetch_one(query)
    if not user:
        raise BackendException(
            message="Login or password is invalid. Please, try again.",
            code=http_status.HTTP_401_UNAUTHORIZED
        )

    hashed_pass = user.password

    if not verify_password(form_data.password, hashed_pass):
        raise BackendException(
            message="Email or password is invalid. Please, try again.",
            code=http_status.HTTP_401_UNAUTHORIZED
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "user_id": user.user_id
    }


@authorization_router.get("/roles/",
                          name="read_available_roles",
                          response_model=JSENDOutSchema[List[AvailableRolesOut]],
                          summary="Get available roles",
                          responses={200: {"description": "Successful get list of available roles response"}},
                          tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    query = select(Role)
    return {
        "data": await database.fetch_all(query),
        "message": "Got roles"
    }
