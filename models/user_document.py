from datetime import datetime

from docxtpl import DocxTemplate
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, DateTime)

from db import database
from models.service import service
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH)

HOSTEL_BOOKING_TEMPLATE_URL = "hostel_booking_template.docx"

metadata_obj = MetaData()

user_document = Table('user_document', metadata_obj,
          Column('user_document_id', Integer, primary_key=True),
          Column('date_created', DateTime),
          Column('name', VARCHAR(255)),
          Column('content', VARCHAR(255)),
          Column('user_request_id', Integer, ForeignKey("user_request.user_request_id")))


async def generate_document_name(service_id: int) -> str:
    query = service.select().where(service.c.service_id == service_id)
    query_result = await database.fetch_one(query)
    return f"Заява на {query_result.service_name.lower()}"


async def create_user_document_content(**kwargs) -> str:
    if kwargs.get("service_id") == 1:
        path_to_template = TEMPLATES_PATH / HOSTEL_BOOKING_TEMPLATE_URL
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
    query = user_document.insert().values(date_created=date_created, 
                                          name=name,
                                          content=content, 
                                          user_request_id=kwargs.get("user_request_id"))
    return await database.execute(query)
