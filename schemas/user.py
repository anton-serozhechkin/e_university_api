from datetime import datetime

from pydantic import BaseModel


class UsersListView(BaseModel):

    user_id: int
    login: str
    last_vist: datetime = None
    email: str
    role_id: int
    role_name: str
    faculty_name: str  
    faculty_id: int  
