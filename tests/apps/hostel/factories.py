from apps.common.schemas import BaseInSchema
from apps.hostel.models import BedPlace, Commandant, Hostel
from tests.bases import AsyncPersistenceHandler, BaseFactory

from decimal import Decimal
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


class CommandantFactory(BaseFactory):
    """CommandantFactory based on Faker and Pydantic"""

    __model__ = CommandantCreateSchema
    __async_persistence__ = AsyncPersistenceHandler(model=Commandant)


# class HostelCreateSchema(BaseInSchema):
#     hostel_id: int
#     number: int
#     name: str = Field(
#         default="Сінергія", title="Name", max_length=100, example="Сінергія"
#     )
#     city: str = Field(default="Харків", title="City", max_length=100, example="Харків")
#     street: str = Field(
#         default="вул. Клочківська",
#         title="Street",
#         max_length=100,
#         example="вул. Клочківська",
#     )
#     build: str = Field(default="216а", title="Build", max_length=10, example="216а")
#     month_price: Decimal = Field(default=0, title="Month price", max_digits=8, decimal_places=6)
#     university_id: int
#     commandant_id: int
#
#
# class HostelFactory(BaseFactory):
#     """HostelFactory based on Faker and Pydantic"""
#
#     __model__ = HostelCreateSchema
#     __async_persistence__ = AsyncPersistenceHandler(model=Hostel)
