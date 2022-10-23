from pydantic import BaseModel


class BedPlaceOut(BaseModel):
    bed_place_id: int
    bed_place_name: str
