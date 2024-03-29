from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.hostel.handlers import hostel_handler
from apps.hostel.schemas import BedPlaceOut, HostelListOut
from apps.users.schemas import UserOut

hostel_router = APIRouter(
    responses={422: {"model": JSENDFailOutSchema, "description": "ValidationError"}}
)


@hostel_router.get(
    "/{university_id}/hostels/",
    name="read_university_hostels",
    response_model=JSENDOutSchema[List[HostelListOut]],
    summary="Get university hostels",
    responses={
        200: {"description": "Successful get all university hostels response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Hostel application"],
)
async def read_hostels_list(
    request: Request,
    university_id: int,
    user: UserOut = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await hostel_handler.read_hostels_list(
            request=request, university_id=university_id, session=session
        ),
        "message": f"Got hostels list of the university with id {university_id}",
    }


@hostel_router.get(
    "/bed-places/",
    name="read_bed_places",
    response_model=JSENDOutSchema[List[BedPlaceOut]],
    summary="Get bed places list",
    responses={
        200: {"description": "Successful get list of available bed places response"}
    },
    tags=["Hostel application"],
)
async def available_bed_places(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: UserOut = Depends(get_current_user),
):
    return {
        "data": await hostel_handler.read_available_bed_places(
            request=request, session=session
        ),
        "message": "Got available bed places list",
    }
