import pytest
from typing import List

from apps.hostel.models import BedPlace, Commandant, Hostel
from tests.apps.hostel.factories import (
    BedPlaceFactory,
    BedPlaceCreateSchema,
    CommandantCreateSchema,
    CommandantFactory,
)


class TestBedPlace:
    @pytest.mark.asyncio
    async def test_factory(self) -> None:
        bed_place_schema: BedPlaceCreateSchema = BedPlaceFactory.build()
        bed_place: BedPlace = await BedPlaceFactory.create_async()
        bed_places: List[BedPlace] = await BedPlaceFactory.create_batch_async(size=3)

        assert isinstance(bed_place_schema, BedPlaceCreateSchema)
        assert isinstance(bed_place, BedPlace)
        for place in bed_places:
            assert isinstance(place, BedPlace)

    @pytest.mark.asyncio
    async def test__repr__(self) -> None:
        obj: BedPlace = await BedPlaceFactory.create_async()
        result = obj.__repr__()
        expected_result = (
            f'{obj.__class__.__name__}(bed_place_id="{obj.bed_place_id}",'
            f' bed_place_name="{obj.bed_place_name}")'
        )
        assert expected_result == result


class TestCommandant:
    @pytest.mark.asyncio
    async def test_factory(self) -> None:
        commandant_schema: CommandantCreateSchema = CommandantFactory.build()
        commandant: Commandant = await CommandantFactory.create_async()
        commandants: List[Commandant] = await CommandantFactory.create_batch_async(
            size=6
        )

        assert isinstance(commandant_schema, CommandantCreateSchema)
        assert isinstance(commandant, Commandant)
        for person in commandants:
            assert isinstance(person, Commandant)

    @pytest.mark.asyncio
    async def test__repr__(self) -> None:
        obj: Commandant = await CommandantFactory.create_async()
        result = obj.__repr__()
        expected_result = (
            f'{obj.__class__.__name__}(commandant_id="{obj.commandant_id}",'
            f' first_name="{obj.first_name}", middle_name="{obj.middle_name}",'
            f' last_name="{obj.last_name}",'
            f' telephone_number="{obj.telephone_number}")'
        )
        assert expected_result == result


# class TestHostel:
#     @pytest.mark.asyncio
#     async def test_factory(self) -> None:
#         hostel_schema: HostelCreateSchema = HostelFactory.build()
#         hostel: Hostel = await HostelFactory.create_async()
#         hostels: List[Hostel] = await HostelFactory.create_batch_async(
#             size=7
#         )
#
#         assert isinstance(hostel_schema, HostelCreateSchema)
#         assert isinstance(hostel, Hostel)
#         for build in hostels:
#             assert isinstance(build, Hostel)
#
#     @pytest.mark.asyncio
#     async def test__repr__(self) -> None:
#         obj: Hostel = await HostelFactory.create_async()
#         result = obj.__repr__()
#         expected_result = (
#             f'{obj.__class__.__name__}(hostel_id="{obj.hostel_id}",'
#             f' number="{obj.number}", name="{obj.name}", city="{obj.city}",'
#             f' street="{obj.street}", build="{obj.build}",'
#             f' month_price="{obj.month_price}", university_id="{obj.university_id}",'
#             f' commandant_id="{obj.commandant_id}")'
#         )
#         assert expected_result == result
