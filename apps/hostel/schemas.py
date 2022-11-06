from apps.common.schemas import BaseOutSchema

from typing import Dict


class HostelListOut(BaseOutSchema):
    university_id: int
    hostel_id: int
    number: int
    name: str
    city: str
    street: str
    build: str
    commandant_id: int
    commandant_full_name: Dict[str, str]


class BedPlaceOut(BaseOutSchema):
    bed_place_id: int
    bed_place_name: str
