from db import database
from schemas.user_documents import DocumentsListOut
from models.user_documents_view import user_documents_view
from handlers.current_user import get_current_user

from typing import List

from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/{university_id}/user-documents/", response_model=List[DocumentsListOut], tags=["Student dashboard"])
async def read_user_documents_list(university_id: int, user = Depends(get_current_user)):
    query = user_documents_view.select().where(user_documents_view.c.university_id == university_id)                               
    return await database.fetch_all(query)

