from apps.users.models import User, UserFaculty, OneTimeToken, Student
from tests.apps.users.factories import (
    UserFactory,
    UserFacultyFactory,
    OneTimeTokenFactory,
    StudentFactory,
)
from tests.bases import BaseModelFactory


class TestUser:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=UserFactory, model=User)

    def test__repr__(self) -> None:
        obj: User = UserFactory()
        expected_result = (
            f'{obj.__class__.__name__}(user_id="{obj.user_id}", login="{obj.login}",'
            f' password="{obj.password}", last_visit_at="{obj.last_visit_at}",'
            f' email="{obj.email}", is_active="{obj.is_active}",'
            f' role_id="{obj.role_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestOneTimeToken:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=OneTimeTokenFactory, model=OneTimeToken)

    def test__repr__(self) -> None:
        obj: OneTimeToken = OneTimeTokenFactory()
        expected_result = (
            f'{obj.__class__.__name__}(token_id="{obj.token_id}",'
            f' token="{obj.token}", expires_at="{obj.expires_at}",'
            f' student_id="{obj.student_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestStudent:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=StudentFactory, model=Student)

    def test__repr__(self) -> None:
        obj: Student = StudentFactory()
        expected_result = (
            f'{obj.__class__.__name__}(student_id="{obj.student_id}",'
            f' first_name="{obj.first_name}", middle_name="{obj.middle_name}",'
            f' last_name="{obj.last_name}",'
            f' telephone_number="{obj.telephone_number}", gender="{obj.gender}",'
            f' course_id="{obj.course_id}", speciality_id="{obj.speciality_id}",'
            f' user_id="{obj.user_id}", faculty_id="{obj.faculty_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestUserFaculty:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=UserFacultyFactory, model=UserFaculty)

    def test__repr__(self) -> None:
        obj: UserFaculty = UserFacultyFactory()
        expected_result = (
            f'{obj.__class__.__name__}(user_id="{obj.user_id}",'
            f' faculty_id="{obj.faculty_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result
