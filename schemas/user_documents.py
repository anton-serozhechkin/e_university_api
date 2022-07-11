from datetime import datetime

from pydantic import BaseModel

class DocumentsListOut(BaseModel):
    university_id: int
    user_id: int
    user_document_id: int
    name: str
    date_created: datetime
    content: str
    