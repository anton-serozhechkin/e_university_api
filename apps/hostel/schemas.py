from apps.common.schemas import BaseOutSchema, FullNameSchema

from apps.hostel.enums import BedPlaceItem


class HostelListOut(BaseOutSchema):
    university_id: int
    hostel_id: int
    number: int
    name: str
    city: str
    street: str
    build: str
    commandant_id: int
    commandant_full_name: FullNameSchema


class BedPlaceOut(BaseOutSchema):
    bed_place_id: BedPlaceItem = [BedPlaceItem.FIRST_OPTION, BedPlaceItem.SECOND_OPTION, BedPlaceItem.THIRD_OPTION]
    bed_place_name: str
