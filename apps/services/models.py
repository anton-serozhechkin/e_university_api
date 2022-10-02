from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, FLOAT, ForeignKey, DateTime)
from db import database
from settings.globals import (TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH, DATETIME_FORMAT)

from datetime import datetime
import os

from docxtpl import DocxTemplate


metadata_obj = MetaData()


service = Table('service', metadata_obj,
          Column('service_id', Integer, primary_key=True),
          Column('service_name', VARCHAR(255)))


user_request = Table('user_request', metadata_obj,
          Column('user_request_id', Integer, primary_key=True),
          Column('user_id', Integer, ForeignKey("user.user_id")),
          Column('service_id', Integer, ForeignKey("service.service_id")),
          Column('date_created', DateTime),
          Column('comment', VARCHAR(255)),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id")),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('status_id', Integer, ForeignKey("status.status_id")))


STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}

user_request_status = Table('user_request_status', metadata_obj,
          Column('status_id', Integer, primary_key=True),
          Column('status_name', VARCHAR(50)))


requisites = Table('requisites', metadata_obj,
          Column('iban', VARCHAR(100)),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('organisation_code', VARCHAR(50)),
          Column('service_id', Integer, ForeignKey("service.service_id")),
          Column('payment_recognation', VARCHAR(255)))


async def generate_document_name(service_id: int) -> str:
    query = service.select().where(service.c.service_id == service_id)
    query_result = await database.fetch_one(query)
    return f"Заява на {query_result.service_name.lower()}"


async def create_user_document_content(*args, **kwargs) -> str:
    if kwargs.get("service_id") == 1:
        path_to_template = os.path.join(TEMPLATES_PATH, "hostel_booking_template.docx")
        doc = DocxTemplate(path_to_template)
        context = kwargs.get("context")
        doc.render(context)
        document_name = f"hostel_settlement_{kwargs.get('date_created')}_{kwargs.get('user_request_id')}.docx"
        path_to_storage = os.path.join(SETTLEMENT_HOSTEL_PATH, document_name)
        doc.save(path_to_storage)
    return path_to_storage


async def create_user_document(*args, **kwargs):
    service_id = kwargs.get("service_id")
    name = await generate_document_name(service_id)
    date_created = datetime.strptime(datetime.now().strftime(DATETIME_FORMAT), DATETIME_FORMAT)
    kwargs["date_created"] = date_created
    content = await create_user_document_content(**kwargs)
    query = user_document.insert().values(date_created=date_created, 
                                          name=name,
                                          content=content, 
                                          user_request_id=kwargs.get("user_request_id"))
    return await database.execute(query)


user_request_review = Table('user_request_review', metadata_obj,
          Column('user_request_review_id', Integer, primary_key=True),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('user_request_id', Integer, ForeignKey("user_request.user_request_id")),
          Column('date_created', DateTime),
          Column('reviewer', Integer, ForeignKey("user.user_id")),
          Column('hostel_id', Integer, ForeignKey("hostel.hostel_id")),
          Column('room_number', Integer),
          Column('start_date_accommodation', DateTime),
          Column('end_date_accommodation', DateTime),
          Column('total_sum', FLOAT),
          Column('payment_deadline', DateTime),
          Column('remark', VARCHAR(255)),
          Column('date_review', DateTime),
          Column('bed_place_id', Integer, ForeignKey("bed_places.bed_place_id")))



user_document = Table('user_document', metadata_obj,
          Column('user_document_id', Integer, primary_key=True),
          Column('date_created', DateTime),
          Column('name', VARCHAR(255)),
          Column('content', VARCHAR(255)),
          Column('user_request_id', Integer, ForeignKey("user_request.user_request_id")))
