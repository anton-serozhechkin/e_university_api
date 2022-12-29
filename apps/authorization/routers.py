from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.handlers import authorization_handler
from apps.authorization.schemas import AvailableRolesOut
from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.users.schemas import AuthOut

authorization_router = APIRouter()


@authorization_router.post(
    "/login",
    name="login",
    response_model=AuthOut,
    summary="Create access and refresh user token",
    responses={
        200: {"description": "Login and refresh user token"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
        401: {"model": JSENDFailOutSchema, "description": "Not authorized response"},
    },
    tags=["Authorization"],
)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    """**Login user**.

    **Input:**
    - **username:** login, which consists of name and random number; required
    - **password:** password to this login name; required

    **Return:**
    - **access_token:** token for access to endpoints
    - **refresh_token:** token for refresh access token
    - **user_id:** id of logined user
    """
    return await authorization_handler.login(
        request=request, form_data=form_data, session=session
    )


@authorization_router.get(
    "/roles/",
    name="read_available_roles",
    response_model=JSENDOutSchema[List[AvailableRolesOut]],
    summary="Get available roles",
    responses={200: {"description": "Successful get list of available roles response"}},
    tags=["SuperAdmin dashboard"],
)
async def available_roles(
    request: Request,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await authorization_handler.available_roles(
            request=request, session=session
        ),
        "message": "Got roles",
    }
