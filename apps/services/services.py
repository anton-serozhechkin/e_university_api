from apps.common.db import database
from apps.services.models import Service, UserDocument
from apps.common.file_manager import file_manager
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH)

from datetime import datetime
from pathlib import Path
from sqlalchemy import select, insert


HOSTEL_BOOKING_TEMPLATE = "hostel_booking_template.docx"


async def generate_document_name(service_id: int) -> str:
    query = select(Service).where(Service.service_id == service_id)
    query_result = await database.fetch_one(query)
    return f"Заява на {query_result.service_name.lower()}"


async def create_user_document_content(**kwargs) -> str:
    if kwargs.get("service_id") == 1:
        user_id = kwargs.get("context").user_id
        DOCUMENT_PATH = SETTLEMENT_HOSTEL_PATH / str(user_id)
        Path(DOCUMENT_PATH).mkdir(exist_ok=True)
        rendered_template = file_manager.render(TEMPLATES_PATH, HOSTEL_BOOKING_TEMPLATE, kwargs.get("context"))
        document_name = f"hostel_settlement_{kwargs.get('date_created')}_{kwargs.get('user_request_id')}.docx"
        document_path = file_manager.create(DOCUMENT_PATH, document_name.replace(":", "-"), rendered_template)
        return document_path
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
