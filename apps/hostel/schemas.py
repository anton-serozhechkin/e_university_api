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
    commandant_full_name: str


class BedPlacesOut(BaseModel):
    bed_place_id: int
    bed_place_name: str
