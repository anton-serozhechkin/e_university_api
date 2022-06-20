from datetime import timedelta
from schemas.user import UsersListView
from models.faculty import faculty as faculty_table
from models.user_list_view import user_list_view
from handlers.current_user import get_current_user
from db import database
from pydantic import BaseModel, validator

from typing import List
import re

from fastapi import Depends, APIRouter 

router = APIRouter()


@router.get("/{univesity_id}/users-list/", response_model=List[UsersListView])
async def users_list(university_id: int, user = Depends(get_current_user)):
    query = user_list_view.select().where(user_list_view.c.university_id == university_id)
    response = await database.fetch_all(query)
    print(response)
    return response
    
    
       
