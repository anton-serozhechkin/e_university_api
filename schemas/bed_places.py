from pydantic import BaseModel


class BedPlacesOut(BaseModel):
    bed_place_id: int
    bed_place_name: str