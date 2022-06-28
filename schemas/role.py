from pydantic import BaseModel

class AvailableRoleOut(BaseModel):
    role_id: int
    role_name: str
