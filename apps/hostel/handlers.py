from apps.common.db import database
from apps.hostel.models import BedPlace, hostel_list_view
from apps.hostel.schemas import HostelListOut, BedPlaceOut

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HostelHandler:

    async def read_hostels_list(self,
                                *,
                                request: Request,
                                university_id: int,
                                session: AsyncSession,
                                ) -> HostelListOut:
        query = select(hostel_list_view).where(hostel_list_view.c.university_id == university_id)
        return await database.fetch_all(query)


    async def read_available_bed_places(self,
                                        *,
                                        request: Request,
                                        session: AsyncSession) -> BedPlaceOut:
        query = select(BedPlace)
        return await database.fetch_all(query)


hostel_handler = HostelHandler()
