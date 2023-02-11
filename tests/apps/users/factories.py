import factory
from pytz import utc

from apps.authorization.services import get_hashed_password
from apps.users.models import OneTimeToken, Student, User, UserFaculty
from tests.apps.educational_institution.factories import (
    CourseFactory,
    FacultyFactory,
    SpecialityFactory,
)
from tests.bases import BaseModelFactory


class UserFactory(BaseModelFactory):
    user_id = factory.Sequence(lambda x: x + 3000)
    mod_login = factory.Faker("pystr", min_chars=1, max_chars=40)
    login = factory.LazyAttribute(function=lambda obj: obj.mod_login + str(obj.user_id))
    simple_password = factory.Faker("pystr", min_chars=4, max_chars=10)
    password = factory.LazyAttribute(
        function=lambda obj: get_hashed_password(obj.simple_password)
    )
    last_visit_at = factory.Faker("date_time", tzinfo=utc)
    mod_email = factory.Faker("email")
    email = factory.LazyAttribute(function=lambda obj: str(obj.user_id) + obj.mod_email)
    is_active = factory.Faker("pybool")
    role_id = factory.SelfAttribute(attribute_name="role.role_id")
    role = factory.SubFactory(factory="tests.apps.authorization.factories.RoleFactory")
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    student = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.StudentFactory",
        factory_related_name="user",
        size=0,
    )
    user_request_reviews = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestReviewFactory",
        factory_related_name="user",
        size=0,
    )
    faculties = factory.RelatedFactoryList(
        factory="tests.apps.educational_institution.factories.FacultyFactory",
        factory_related_name="user",
        size=0,
    )
    user_requests = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestFactory",
        factory_related_name="user",
        size=0,
    )
    user_faculties = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.UserFacultyFactory",
        factory_related_name="user",
        size=0,
    )

    @classmethod
    def _setup_next_sequence(cls):
        return 1

    class Meta:
        model = User
        exclude = (
            "role",
            "simple_password",
            "mod_login",
            "mod_email",
            "student",
            "user_request_reviews",
            "faculties",
            "user_requests",
            "user_faculties",
        )
        sqlalchemy_get_or_create = (
            "email",
            "login",
            "role_id",
        )


class OneTimeTokenFactory(BaseModelFactory):
    token_id = factory.Sequence(lambda x: x + 3000)
    token = factory.Faker("pystr", min_chars=1, max_chars=255)
    expires_at = factory.Faker("date_time", tzinfo=utc)
    student_id = factory.SelfAttribute(attribute_name="student.student_id")
    student = factory.SubFactory(factory="tests.apps.users.factories.StudentFactory")

    @classmethod
    def _setup_next_sequence(cls):
        return 1

    class Meta:
        model = OneTimeToken
        exclude = ("student",)
        sqlalchemy_get_or_create = ("student_id",)


class StudentFactory(BaseModelFactory):
    student_id = factory.Sequence(lambda x: x + 3000)
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    mod_tel_number = factory.Faker("pystr", min_chars=1, max_chars=10)
    telephone_number = factory.LazyAttribute(
        function=lambda obj: str(obj.student_id) + obj.mod_tel_number
    )
    gender = factory.Faker("pystr", min_chars=1, max_chars=1)
    course_id = factory.SelfAttribute(attribute_name="course.course_id")
    course = factory.SubFactory(factory=CourseFactory)
    speciality_id = factory.SelfAttribute(attribute_name="speciality.speciality_id")
    speciality = factory.SubFactory(factory=SpecialityFactory)
    user_id = factory.SelfAttribute(attribute_name="user.user_id")
    user = factory.SubFactory(factory=UserFactory)
    faculty_id = factory.SelfAttribute(attribute_name="faculty.faculty_id")
    faculty = factory.SubFactory(factory=FacultyFactory)
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    one_time_token = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.OneTimeTokenFactory",
        factory_related_name="user_request",
        size=0,
    )

    @classmethod
    def _setup_next_sequence(cls):
        return 1

    class Meta:
        model = Student
        exclude = (
            "course",
            "speciality",
            "mod_tel_number",
            "user",
            "faculty",
            "one_time_token",
        )
        sqlalchemy_get_or_create = (
            "course_id",
            "user_id",
            "faculty_id",
            "speciality_id",
            "telephone_number",
        )


class UserFacultyFactory(BaseModelFactory):
    user_id = factory.SelfAttribute(attribute_name="user.user_id")
    faculty_id = factory.SelfAttribute(attribute_name="faculty.faculty_id")
    user = factory.SubFactory(factory=UserFactory)
    faculty = factory.SubFactory(factory=FacultyFactory)

    @classmethod
    def _setup_next_sequence(cls):
        return 1

    class Meta:
        model = UserFaculty
        exclude = ("user", "faculty")
        sqlalchemy_get_or_create = ("user_id", "faculty_id")
