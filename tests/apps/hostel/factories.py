from apps.common.schemas import BaseInSchema
from apps.hostel.models import BedPlace, Commandant, Hostel
from apps.hostel.schemas import BedPlaceOut, HostelListOut
from tests.bases import AsyncPersistenceHandler, BaseFactory

from pydantic import Field, validator
from typing import Optional


class BedPlaceCreateSchema(BaseInSchema):
    bed_place_id: int
    bed_place_name: str = Field(max_length=50)


class BedPlaceFactory(BaseFactory):
    """BedPlaceFactory based on Faker and Pydantic"""

    __model__ = BedPlaceCreateSchema
    __async_persistence__ = AsyncPersistenceHandler(model=BedPlace)


class CommandantCreateSchema(BaseInSchema):
    commandant_id: int
    last_name: str = Field(
        title="Last name", max_length=50, example="Петренко"
    )
    first_name: str = Field(
        title="First name", max_length=50, example="Петро"
    )
    middle_name: Optional[str] = Field(
        default=None, title="Middle name", max_length=50, example="Петрович"
    )
    telephone_number: str = Field(
        title="Telephone number",
        max_length=12,
        min_length=12,
        example="380971111111",
    )

    # @validator("last_name")
    # def validate_last_name(cls, value: str) -> str:
    #     if not value:
    #         raise ValueError("The student's surname is mandatory")
    #     if not value.istitle():
    #         raise ValueError("The last name first letter must be uppercase")
    #     return value
    #
    # @validator("first_name")
    # def validate_first_name(cls, value: str) -> str:
    #     if not value:
    #         raise ValueError("The student's name is mandatory")
    #     if not value.istitle():
    #         raise ValueError("The name first letter must be uppercase")
    #     return value
    #
    # @validator("middle_name")
    # def validate_middle_name(cls, value: str) -> Optional[str]:
    #     if value:
    #         if not value.istitle():
    #             raise ValueError("The middle name first letter must be uppercase")
    #         return value
    #
    # @validator("telephone_number")
    # def validate_telephone_number(cls, value: str) -> str:
    #     if not value.isdigit():
    #         raise ValueError("The phone number must consist of digits")
    #     return value


class CommandantFactory(BaseFactory):
    """CommandantFactory based on Faker and Pydantic"""

    __model__ = CommandantCreateSchema
    __async_persistence__ = AsyncPersistenceHandler(model=Commandant)


