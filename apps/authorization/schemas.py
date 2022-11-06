from apps.common.schemas import BaseOutSchema


class AvailableRolesOut(BaseOutSchema):
    role_id: int
    role_name: str
