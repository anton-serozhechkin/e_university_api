from models.user_faculty import user_faculty as user_faculty_table
from models.user_request import user_request as user_request_table
from models.user_request_exist_view import user_request_exist_view
from models.status import STATUS_MAPPING
from schemas.user_request import (CreateUserRequestIn, CreateUserRequestOut, 
                                  UserRequestExistenceOut)
from handlers.current_user import get_current_user
from db import database

from datetime import datetime

from fastapi import Depends, APIRouter


router = APIRouter()


@router.get("/{university_id}/user-request-existence/{service_id}/", response_model=UserRequestExistenceOut, tags=["Student dashboard"])
async def check_user_request_existence(university_id: int, service_id: int, user = Depends(get_current_user)):
    query = user_request_exist_view.select().where(user_request_exist_view.c.user_id == user.user_id, 
                                            user_request_exist_view.c.university_id == university_id, 
                                            user_request_exist_view.c.service_id == service_id)
    user_request_result = await database.fetch_one(query)
    if user_request_result:
        response = {
            "user_request_id": user_request_result.user_request_id,
            "status_id": user_request_result.status_id,
            "user_request_exist": True
        }
    else:
        response = {
            "user_request_id": None,
            "status_id": None,
            "user_request_exist": False
        }
    return response

@router.post("/{university_id}/create-user-request/", response_model=CreateUserRequestOut, tags=["Student dashboard"])
async def create_user_request(university_id: int, user_request: CreateUserRequestIn, user = Depends(get_current_user)):
    query = user_faculty_table.select().where(user_faculty_table.c.user_id == user.user_id)
    user_faculty_result = await database.fetch_one(query)
    query = user_request_table.insert().values(user_id=user.user_id, 
                                                service_id=user_request.service_id,
                                                date_created=datetime.now(),
                                                comment=user_request.comment, 
                                                faculty_id=user_faculty_result.faculty_id,
                                                university_id=university_id,
                                                status_id=STATUS_MAPPING.get("Розглядається"))

    last_record_id = await database.execute(query)
    return {
        "status_id": STATUS_MAPPING.get("Розглядається"),
        "user_request_id": last_record_id
    }
