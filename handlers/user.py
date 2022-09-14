from schemas.user import UsersListViewOut, CreateUserIn, CreateUserOut, DeleteUserIn
from models.user_list_view import user_list_view
from models.user import user as user_table
from models.user_faculty import user_faculty
from handlers.current_user import get_current_user
from components.utils import get_hashed_password
from db import database

from random import randint
from typing import List

from fastapi import Depends, APIRouter 


router = APIRouter()


@router.get("/{university_id}/users/", response_model=List[UsersListViewOut], tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user = Depends(get_current_user)):
    query = user_list_view.select().where(user_list_view.c.university_id == university_id)
    response = await database.fetch_all(query)
    return response


@router.post("/{university_id}/users/", response_model=CreateUserOut, tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth = Depends(get_current_user)):
    
    CreateUserIn(
        email=user.email,
        password=user.password,
        password_re_check = user.password_re_check,
        role_id =  user.role_id,
        faculty_id = user.faculty_id
    )

    hashed_password = get_hashed_password(user.password)

    login = f"{(user.email[:4])}-{randint(100,999)}".lower()

    query = user_table.insert().values(login=login, password=hashed_password, 
                                        email=user.email, role_id=user.role_id, 
                                        is_active=False)

    last_record_id = await database.execute(query)

    for faculty_id in user.faculty_id:
        query = user_faculty.insert().values(user_id=last_record_id, 
                                            faculty_id = faculty_id)
        await database.execute(query)

    return {
       "user_id": last_record_id
    }


@router.delete("/{university_id}/users/", tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth = Depends(get_current_user)):
    query = user_table.delete().where(user_table.c.user_id == delete_user.user_id)
    
    await database.fetch_one(query)

    return {
        "user_id": delete_user.user_id
    }