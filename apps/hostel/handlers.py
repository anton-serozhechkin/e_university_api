from apps.common.db import database
from apps.hostel.models import BedPlace, hostel_list_view

from sqlalchemy import select


async def get_hostels(university_id: int):
    query = select(hostel_list_view).where(hostel_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


async def get_available_bed_places():
    query = select(BedPlace)
    return await database.fetch_all(query)
