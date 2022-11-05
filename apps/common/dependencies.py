from apps.common.db import async_session_factory, session_factory
from apps.common.exceptions import BackendException
from apps.common.exception_handlers import integrity_error_handler
from apps.users.schemas import TokenPayload, UserOut
from apps.users.services import user_service, user_list_service
from settings import Settings

from datetime import datetime
from fastapi import Depends, HTTPException, status as http_status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import typing


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    """Creates FastAPI dependency for generation of SQLAlchemy AsyncSession.
    Yields:
        AsyncSession: SQLAlchemy AsyncSession.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except IntegrityError as error:
            await session.rollback()
            integrity_error_handler(error=error)
        finally:
            await session.close()


def get_session() -> typing.Generator[Session, None, None]:
    """Creates FastAPI dependency for generation of SQLAlchemy Session.
    Yields:
        Session: SQLAlchemy Session.
    """
    with session_factory() as session:
        try:
            yield session
        except IntegrityError as error:
            session.rollback()
            integrity_error_handler(error=error)
        finally:
            session.close()


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(
        token: str = Depends(reusable_oauth),
        session: AsyncSession = Depends(get_async_session)) -> UserOut:
    try:
        payload = jwt.decode(
            token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Token data has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Credential verification failed",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await user_service.read(session=session, data={"email": token_data.sub})
    if user is None:
        raise BackendException(
            message="User not found",
            code=http_status.HTTP_404_NOT_FOUND
        )
    return await user_list_service.read(session=session, data={"user_id": user.user_id})
