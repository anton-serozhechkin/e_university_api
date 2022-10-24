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
    commandant_first_name: str
    commandant_last_name: str
    commandant_middle_name: str
