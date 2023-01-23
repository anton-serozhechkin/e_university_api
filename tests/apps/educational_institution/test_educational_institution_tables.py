from apps.educational_institutions.models import (
    Course,
    Dean,
    Faculty,
    Rector,
    Speciality,
    University,
)
from tests.apps.educational_institution.factories import (
    CourseFactory,
    DeanFactory,
    FacultyFactory,
    RectorFactory,
    SpecialityFactory,
    UniversityFactory,
)
from tests.bases import BaseModelFactory


class TestRector:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=RectorFactory, model=Rector)

    def test__repr__(self) -> None:
        obj: Rector = RectorFactory()
        expected_result = (
            f'{obj.__class__.__name__}(rector_id="{obj.rector_id}",'
            f' first_name="{obj.first_name}", middle_name="{obj.middle_name}",'
            f' last_name="{obj.last_name}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestUniversity:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(
            factory_class=UniversityFactory, model=University
        )

    def test__repr__(self) -> None:
        obj: University = UniversityFactory()
        expected_result = (
            f'{obj.__class__.__name__}(university_id="{obj.university_id}", '
            f'university_name="{obj.university_name}", city="{obj.city}", '
            f'logo="{obj.logo}", rector_id="{obj.rector_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestFaculty:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=FacultyFactory, model=Faculty)

    def test__repr__(self) -> None:
        obj: Faculty = FacultyFactory()
        expected_result = (
            f'{obj.__class__.__name__}(faculty_id="{obj.faculty_id}",'
            f' name="{obj.name}", shortname="{obj.shortname}",'
            f' main_email="{obj.main_email}", dean_id="{obj.dean_id}",'
            f' university_id="{obj.university_id}"'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestSpeciality:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(
            factory_class=SpecialityFactory, model=Speciality
        )

    def test__repr__(self) -> None:
        obj: Speciality = SpecialityFactory()
        expected_result = (
            f'{obj.__class__.__name__}(speciality_id="{obj.speciality_id}",'
            f' code="{obj.code}", name="{obj.name}", faculty_id="{obj.faculty_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestDean:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=DeanFactory, model=Dean)

    def test__repr__(self) -> None:
        obj: Dean = DeanFactory()
        expected_result = (
            f'{obj.__class__.__name__}(dean_id="{obj.dean_id}",'
            f' first_name="{obj.first_name}", middle_name="{obj.middle_name}",'
            f' last_name="{obj.last_name}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestCourse:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=CourseFactory, model=Course)

    def test__repr__(self) -> None:
        obj: Course = CourseFactory()
        expected_result = (
            f'{obj.__class__.__name__}(course_id="{obj.course_id}",'
            f' value="{obj.value}")'
        )
        result = obj.__repr__()
        assert expected_result == result
