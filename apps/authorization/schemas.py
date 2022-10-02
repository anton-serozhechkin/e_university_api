from pydantic import BaseModel

class AvailableRolesOut(BaseModel):
    role_id: int
    role_name: str