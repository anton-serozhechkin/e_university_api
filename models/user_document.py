from models import user_request
from models.service import Service

from datetime import datetime

from docxtpl import DocxTemplate
from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, DATETIME, select, insert)
from sqlalchemy.orm import relationship

from db import database, Base
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH)

HOSTEL_BOOKING_TEMPLATE_URL = "hostel_booking_template.docx"


class UserDocument(Base):
    __tablename__ = "user_document"

    user_document_id = Column(INTEGER, primary_key=True, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    content = Column(VARCHAR(length=255), nullable=False)
    user_request_id = Column(INTEGER, ForeignKey("user_request.user_request_id"), nullable=False)

    user_request = relationship("UserRequest", back_populates="user_documents")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_document_id="{self.user_document_id}", date_created="{self.date_created}", ' \
               f'name="{self.name}", content="{self.content}", user_request_id="{self.user_request_id}")'


async def generate_document_name(service_id: int) -> str:
    query = select(Service).where(Service.service_id == service_id)
    query_result = await database.fetch_one(query)
    return f"Заява на {query_result.service_name.lower()}"


async def create_user_document_content(**kwargs) -> str:
    if kwargs.get("service_id") == 1:
        path_to_template = TEMPLATES_PATH / HOSTEL_BOOKING_TEMPLATE_URL     #   TODO NameError
        doc = DocxTemplate(path_to_template)
        context = kwargs.get("context")
        doc.render(context)
        document_name = f"hostel_settlement_{kwargs.get('date_created')}_{kwargs.get('user_request_id')}.docx"
        path_to_storage = SETTLEMENT_HOSTEL_PATH / document_name
        doc.save(path_to_storage)
        return str(path_to_storage)
    raise RuntimeError(f"create_user_document_content({kwargs}) | there is no service_id!!!")


async def create_user_document(**kwargs):
    service_id = kwargs.get("service_id")
    name = await generate_document_name(service_id)
    date_created = datetime.strptime(datetime.now().strftime(Settings.DATETIME_FORMAT),
                                     Settings.DATETIME_FORMAT)
    kwargs["date_created"] = date_created
    content = await create_user_document_content(**kwargs)
    query = insert(UserDocument).values(date_created=date_created,
                                        name=name,
                                        content=content,
                                        user_request_id=kwargs.get("user_request_id"))
    return await database.execute(query)
