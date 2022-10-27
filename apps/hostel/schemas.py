from pydantic import BaseModel


class HostelListOut(BaseModel):
    university_id: int
    hostel_id: int
    number: int
    name: str
    city: str
    street: str
    build: str
    commandant_id: int
    first_name: str
    last_name: str
    middle_name: str


class BedPlaceOut(BaseModel):
    bed_place_id: int
    bed_place_name: str
