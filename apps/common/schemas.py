from datetime import datetime
from typing import Generic, TypeVar, Union

from fastapi import status as http_status
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.typing import NoneType

from apps.common.enums import JSENDStatus

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
    date_created: datetime


class HostelNameSchema(BaseOutSchema):
    name: str = None
    number: int = None


class FullNameSchema(BaseOutSchema):
    last_name: str
    first_name: str
    middle_name: str = None
