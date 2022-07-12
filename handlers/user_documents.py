from cgi import test
from fileinput import filename
from db import database
import os 
from schemas.user_documents import DocumentsListOut, DocumentsList
from models.user_documents_view import user_documents_view
from handlers.current_user import get_current_user

from typing import List
from io import StringIO 

from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.responses import FileResponse
from docx import Document

router = APIRouter()

@router.get("/{university_id}/user-documents/", response_model=List[DocumentsListOut], tags=["Student dashboard"])
async def read_user_documents_list(university_id: int, user = Depends(get_current_user)):
    query = user_documents_view.select().where(user_documents_view.c.university_id == university_id)                               
    return await database.fetch_all(query)
   


@router.post("/{university_id}/documents/", response_class=FileResponse, tags=["Student dashboard"])
async def read_user_documents(university_id: int, user_documents: DocumentsList, user = Depends(get_current_user)):
    with open(user_documents.file_path, 'r') as f:
        source_stream = StringIO(f.read())
        contents = Document(source_stream)


    if os.path.exists(user_documents.file_path):
        return FileResponse(contents, media_type='application/octet-stream', filename="test")
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл не знайдено")
