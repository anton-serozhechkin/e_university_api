from apps.hostel.schemas import HostelListOut, BedPlaceOut
from apps.hostel.services import hostel_service, bed_place_service

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class HostelHandler:
    async def read_hostels_list(
        self,
        *,
        request: Request,
        university_id: int,
        session: AsyncSession,
    ) -> HostelListOut:
        return await hostel_service.list(
            session=session, filters={"university_id": university_id}
        )

    async def read_available_bed_places(
        self, *, request: Request, session: AsyncSession
    ) -> List[BedPlaceOut]:
        return await bed_place_service.list(session=session)


hostel_handler = HostelHandler()
