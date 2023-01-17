import os
from datetime import datetime
from mimetypes import MimeTypes
from typing import Dict, Generic, List, Optional, TypeVar, Union

from fastapi import status as http_status
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.generics import GenericModel
from pydantic.typing import NoneType
from starlette.datastructures import UploadFile

from apps.common.enums import JSENDStatus, MultipartSubtypeEnum
from apps.common.exceptions import WrongFile

SchemaVar = TypeVar("SchemaVar", bound=Union[BaseModel, NoneType, str])


class BaseInSchema(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True
        allow_population_by_field_name = True
        use_enum_values = True


class BaseOutSchema(BaseInSchema):
    pass


class JSENDOutSchema(GenericModel, Generic[SchemaVar]):
    status: JSENDStatus = Field(default=JSENDStatus.SUCCESS)
    data: SchemaVar
    message: str
    code: int = Field(default=http_status.HTTP_200_OK)


class JSENDFailOutSchema(JSENDOutSchema):
    status: JSENDStatus = Field(default=JSENDStatus.FAIL)
    data: Union[str, NoneType]
    code: int = Field(default=http_status.HTTP_400_BAD_REQUEST)


class JSENDErrorOutSchema(JSENDOutSchema):
    status: JSENDStatus = Field(default=JSENDStatus.ERROR)
    data: Union[str, NoneType]
    code: int = Field(default=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDocumentsSchema(BaseOutSchema):
    id: int
    name: str
    created_at: datetime


class HostelNameSchema(BaseOutSchema):
    name: str = None
    number: int = None


class FullNameSchema(BaseOutSchema):
    last_name: str
    first_name: str
    middle_name: str = None


class MessageSchema(BaseModel):
    recipients: List[EmailStr]
    attachments: List[Union[UploadFile, Dict, str]] = []
    subject: str = ""
    body: Optional[Union[str, list]] = None
    template_body: Optional[Union[list, dict]] = None
    html: Optional[Union[str, List, Dict]] = None
    cc: List[EmailStr] = []
    bcc: List[EmailStr] = []
    reply_to: List[EmailStr] = []
    charset: str = "utf-8"
    subtype: Optional[str] = None
    multipart_subtype: MultipartSubtypeEnum = MultipartSubtypeEnum.mixed
    headers: Optional[Dict] = None

    @validator("attachments")
    def validate_file(cls, v):
        temp = []
        mime = MimeTypes()

        for file in v:
            file_meta = None
            if isinstance(file, dict):
                keys = file.keys()
                if "file" not in keys:
                    raise WrongFile('missing "file" key')
                file_meta = dict.copy(file)
                del file_meta["file"]
                file = file["file"]
            if isinstance(file, str):
                if (
                    os.path.isfile(file)
                    and os.access(file, os.R_OK)
                    and validate_path(file)
                ):
                    mime_type = mime.guess_type(file)
                    f = open(file, mode="rb")
                    _, file_name = os.path.split(f.name)
                    u = UploadFile(file_name, f, content_type=mime_type[0])
                    temp.append((u, file_meta))
                else:
                    raise WrongFile(
                        "incorrect file path for attachment or not readable"
                    )
            elif isinstance(file, UploadFile):
                temp.append((file, file_meta))
            else:
                raise WrongFile(
                    "attachments field type incorrect, must be UploadFile or path"
                )
        return temp

    @validator("subtype")
    def validate_subtype(cls, value, values, config, field):
        """Validate subtype field."""
        if values["template_body"]:
            return "html"
        return value

    class Config:
        arbitrary_types_allowed = True


def validate_path(path):
    cur_dir = os.path.abspath(os.curdir)
    requested_path = os.path.abspath(os.path.relpath(path, start=cur_dir))
    common_prefix = os.path.commonprefix([requested_path, cur_dir])
    return common_prefix == cur_dir
