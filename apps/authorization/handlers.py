from typing import List

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.schemas import AvailableRolesOut
from apps.authorization.services import (
    create_access_token,
    create_refresh_token,
    role_service,
    verify_password,
    verify_user,
)
from apps.users.schemas import AuthOut
from apps.users.services import user_service


class AuthorizationHandler:
    @staticmethod
    async def login(
        *,
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession,
    ) -> AuthOut:
        user = await user_service.read(
            session=session, data={"login": form_data.username}
        )
        verify_user(user)
        verify_password(user, form_data.password)
        return AuthOut(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
            user_id=user.user_id,
        )

    @staticmethod
    async def available_roles(
        *,
        request: Request,
        session: AsyncSession,
    ) -> List[AvailableRolesOut]:
        return await role_service.list(session=session)


authorization_handler = AuthorizationHandler()
