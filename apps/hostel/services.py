from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult, IteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Table
from typing import Dict, List, Union

from apps.common.services import AsyncCRUDBase
from apps.hostel.models import Hostel, BedPlace, hostel_list_view
from apps.hostel.schemas import BedPlaceOut


class HostelCRUDBase(AsyncCRUDBase):
    async def list(
        self,
        *,
        session: AsyncSession,
        filters: Union[Dict, None] = None  # TODO: Add dynamic filtering system
    ) -> List[Union[Table, BedPlaceOut]]:
        select_statement = select(self.model)
        if filters:
            select_statement = select_statement.filter_by(**filters)
        select_statement = select_statement.execution_options(populate_existing=True)

        result: IteratorResult = await session.execute(statement=select_statement)
        if isinstance(self.model, Table):
            objects: List[Table] = result.all()
        else:
            objects: List[BedPlaceOut] = result.scalars().all()
        return objects


hostel_service = HostelCRUDBase(model=hostel_list_view)
bed_place_service = HostelCRUDBase(model=BedPlace)
