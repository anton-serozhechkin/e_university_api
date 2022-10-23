from sqlalchemy import select, delete, insert

from schemas.user import UsersListViewOut, CreateUserIn, CreateUserOut, DeleteUserIn
from models.user_list_view import user_list_view
from models.user import User
from models.user_faculty import UserFaculty
from handlers.current_user import get_current_user
from components.utils import get_hashed_password
from db import database

from random import randint
from typing import List

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.get("/{university_id}/users/", response_model=JSENDOutSchema[List[UsersListViewOut]],
            tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user=Depends(get_current_user)):
    query = select(user_list_view).where(user_list_view.c.university_id == university_id)
    return {
        "data": await database.fetch_all(query),
        "message": f"Got user list of the university with id {university_id}"
    }


@router.post("/{university_id}/users/", response_model=JSENDOutSchema[CreateUserOut], tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth=Depends(get_current_user)):
    CreateUserIn(
        email=user.email,
        password=user.password,
        password_re_check=user.password_re_check,
        role_id=user.role_id,
        faculty_id=user.faculty_id
    )

    hashed_password = get_hashed_password(user.password)

    login = f"{(user.email[:4])}-{randint(100, 999)}".lower()

    query = insert(User).values(login=login, password=hashed_password,
                                email=user.email, role_id=user.role_id,
                                is_active=False)

    last_record_id = await database.execute(query)

    for faculty_id in user.faculty_id:
        query = insert(UserFaculty).values(user_id=last_record_id,
                                           faculty_id=faculty_id)
        await database.execute(query)

    return {
        "data": {
            "user_id": last_record_id
        },
        "message": f"Created user with id {last_record_id}"
    }


@router.delete("/{university_id}/users/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth=Depends(get_current_user)):
    query = delete(User).where(User.user_id == delete_user.user_id)

    await database.execute(query)

    return {
        "data": {
            "user_id": delete_user.user_id
        },
        "message": f"Deleted user with id {delete_user.user_id}"
    }
