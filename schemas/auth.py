from pydantic import BaseModel


class AuthOut(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
