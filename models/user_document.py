from models.service import service
from db import database

from datetime import datetime
import os

from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, DateTime)
from docxtpl import DocxTemplate

from settings.settings import Settings

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


async def create_user_document_content(*args, **kwargs) -> str:
    if kwargs.get("service_id") == 1:
        path_to_template = os.path.join(Settings.TEMPLATES_PATH, "hostel_booking_template.docx")
        doc = DocxTemplate(path_to_template)
        context = kwargs.get("context")
        doc.render(context)
        document_name = f"hostel_settlement_{kwargs.get('date_created')}_{kwargs.get('user_request_id')}.docx"
        path_to_storage = os.path.join(Settings.SETTLEMENT_HOSTEL_PATH, document_name)
        doc.save(path_to_storage)
    return path_to_storage


async def create_user_document(*args, **kwargs):
    service_id = kwargs.get("service_id")
    name = await generate_document_name(service_id)
    date_created = datetime.strptime(datetime.now().strftime(Settings.DATETIME_FORMAT), Settings.DATETIME_FORMAT)
    kwargs["date_created"] = date_created
    content = await create_user_document_content(**kwargs)
    query = user_document.insert().values(date_created=date_created, 
                                          name=name,
                                          content=content, 
                                          user_request_id=kwargs.get("user_request_id"))
    return await database.execute(query)
