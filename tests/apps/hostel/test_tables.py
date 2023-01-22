
from apps.hostel.models import BedPlace, Hostel, Commandant
from tests.apps.hostel.factories import (
    BedPlaceFactory,
    CommandantFactory,
    HostelFactory
)
from tests.bases import BaseModelFactory


class TestBedPlaces:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=BedPlaceFactory, model=BedPlace)

    def test__repr__(self) -> None:
        obj: BedPlace = BedPlaceFactory()
        expected_result = f'{obj.__class__.__name__}(bed_place_id="{obj.bed_place_id}", ' \
                          f'bed_place_name="{obj.bed_place_name}")'
        result = obj.__repr__()
        assert expected_result == result


class TestCommandant:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=CommandantFactory, model=Commandant)

    def test__repr__(self) -> None:
        obj: Commandant = CommandantFactory()
        expected_result = (
            f'{obj.__class__.__name__}(commandant_id="{obj.commandant_id}",'
            f' first_name="{obj.first_name}", middle_name="{obj.middle_name}",'
            f' last_name="{obj.last_name}",'
            f' telephone_number="{obj.telephone_number}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestHostel:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=HostelFactory, model=Hostel)

    def test__repr__(self) -> None:
        obj: Hostel = HostelFactory()
        expected_result = (
            f'{obj.__class__.__name__}(hostel_id="{obj.hostel_id}",'
            f' number="{obj.number}", name="{obj.name}", city="{obj.city}",'
            f' street="{obj.street}", build="{obj.build}",'
            f' month_price="{obj.month_price}", university_id="{obj.university_id}",'
            f' commandant_id="{obj.commandant_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result
