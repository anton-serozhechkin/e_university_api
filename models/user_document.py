from models.service import service
from db import database

from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, DateTime)


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
    response = f"Заява на {query_result.service_name.lower()}"
    return response
