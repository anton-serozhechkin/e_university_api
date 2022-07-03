from pydantic import BaseModel

class HostelListOut(BaseModel):
    university_id: int
    hostel_id: str
    number: int
    name: str
    city: str
    street: str
    build: str
    commandant_id: int
    commandant_full_name: str