from typing import List

from apps.hostel.models import BedPlace
from tests.apps.hostel.factories import BedPlaceFactory


class TestBedPlace:
    async def test_factory(self) -> None:
        bed_place: BedPlace = await BedPlaceFactory.create_async()
        bed_places: List[BedPlace] = await BedPlaceFactory.create_batch_async(size=2)

        assert isinstance(bed_place, BedPlace)
        for place in bed_places:
            assert isinstance(place, BedPlace)

    async def test__repr__(self) -> None:
        obj: BedPlace = BedPlaceFactory.create_async()
        result = obj.__repr__()
        expected_result = (
            f'{self.__class__.__name__}(bed_place_id="{obj.bed_place_id}",'
            f' bed_place_name="{obj.bed_place_name}")'
        )
        assert expected_result == result
