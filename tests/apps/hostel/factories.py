from typing import Optional

from pydantic import Field

from apps.common.schemas import BaseInSchema
from apps.hostel.models import BedPlace, Commandant
from tests.bases import AsyncPersistenceHandler, BaseFactory


class BedPlaceCreateSchema(BaseInSchema):
    bed_place_id: int
    bed_place_name: str = Field(max_length=50)


class BedPlaceFactory(BaseFactory):
    """BedPlaceFactory based on Faker and Pydantic"""

    __model__ = BedPlaceCreateSchema
    __async_persistence__ = AsyncPersistenceHandler(model=BedPlace)


class CommandantCreateSchema(BaseInSchema):
    commandant_id: int
    last_name: str = Field(title="Last name", max_length=50, example="Petrenko")
    first_name: str = Field(title="First name", max_length=50, example="Petro")
    middle_name: Optional[str] = Field(
        default=None, title="Middle name", max_length=50, example="Petrovych"
    )
    telephone_number: str = Field(
        title="Telephone number",
        max_length=12,
        min_length=12,
        example="380971111111",
    )


class CommandantFactory(BaseFactory):
    """CommandantFactory based on Faker and Pydantic"""

    __model__ = CommandantCreateSchema
    __async_persistence__ = AsyncPersistenceHandler(model=Commandant)
