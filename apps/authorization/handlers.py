from apps.authorization.services import (verify_password, create_access_token, create_refresh_token, verify_user,
                                         role_service)
from apps.users.services import user_service

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


class AuthorizationHandler:

    async def login(
            self,
            *,
            request: Request,
            form_data: OAuth2PasswordRequestForm = Depends(),
            session: AsyncSession):
        user = await user_service.read(session=session, data={"login": form_data.username})
        verify_user(user)
        verify_password(user, form_data.password)
        return {
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
            "user_id": user.user_id
        }

    async def available_roles(
            self,
            *,
            request: Request,
            session: AsyncSession
    ):
        return await role_service.list(session=session)


authorization_handler = AuthorizationHandler()
