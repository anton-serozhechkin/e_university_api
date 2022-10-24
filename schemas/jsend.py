from typing import Generic, TypeVar, Union
from fastapi import status as http_status
from pydantic import Field, BaseModel
from pydantic.generics import GenericModel
from pydantic.typing import NoneType

from components.enums import JSENDStatus


SchemaVar = TypeVar("SchemaVar", bound=Union[BaseModel, NoneType, str])


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
