from apps.users.serivces import get_current_user
from apps.authorization.schemas import AvailableRolesOut
from apps.common.schemas import JSENDOutSchema, JSENDFailOutSchema
from apps.users.schemas import AuthOut
from apps.authorization import handlers

from typing import List
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm


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
    return await handlers.login(form_data)


@authorization_router.get("/roles/",
                          name="read_available_roles",
                          response_model=JSENDOutSchema[List[AvailableRolesOut]],
                          summary="Get available roles",
                          responses={200: {"description": "Successful get list of available roles response"}},
                          tags=["SuperAdmin dashboard"])
async def available_roles(user=Depends(get_current_user)):
    return {
        "data": await handlers.available_roles(),
        "message": "Got roles"
    }
