from typing import List

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.send_email import send_email_async
from apps.hostel.schemas import BedPlaceOut, HostelListOut
from apps.hostel.services import bed_place_service, hostel_service


class HostelHandler:
    @staticmethod
    async def read_hostels_list(
        *,
        request: Request,
        university_id: int,
        session: AsyncSession,
    ) -> HostelListOut:
        return await hostel_service.list(
            session=session, filters={"university_id": university_id}
        )

    @staticmethod
    async def read_available_bed_places(
        *,
        request: Request,
        session: AsyncSession,
    ) -> List[BedPlaceOut]:
        return await bed_place_service.list(session=session)


hostel_handler = HostelHandler()
