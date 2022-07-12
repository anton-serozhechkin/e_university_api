from datetime import datetime

from pydantic import BaseModel

class DocumentsListOut(BaseModel):
    user_document_id: int
    name: str
    date_created: datetime
    content: str
    user_id: int
    university_id: int


class DocumentsList(BaseModel):
    file_path: str
