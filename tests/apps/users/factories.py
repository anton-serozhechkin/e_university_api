from typing import Optional

from pydantic import Field
import random

from pytz import utc
import factory
from apps.common.schemas import BaseInSchema
from apps.services.models import Service, UserRequest, Status, Requisites, UserRequestReview, UserDocument, ServiceDocument
from apps.users.models import User, Student, OneTimeToken, UserFaculty
from tests.bases import AsyncPersistenceHandler, BaseFactory, BaseModelFactory
from tests.apps.educational_institution.factories import UniversityFactory, FacultyFactory, CourseFactory, SpecialityFactory
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory


class UserFactory(BaseModelFactory):
    user_id = factory.Sequence(lambda x: x)
    login = factory.Faker("pystr", min_chars=1, max_chars=50)
    password = factory.Faker("pystr", min_chars=1, max_chars=50)
    last_visit_at = factory.Faker("date_time", tzinfo=utc)
    is_active = factory.Faker("pybool")
    role_id = factory.SelfAttribute(attribute_name="role.role_id")
    role = factory.SubFactory(factory="tests.apps.authorization.factories.RoleFactory")
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    student = factory.RelatedFactory(
        factory="tests.apps.users.factories.StudentFactory",
        factory_related_name="user",
        size=0
    )
    user_request_reviews = factory.RelatedFactory(
        factory="tests.apps.services.factories.UserRequestReviewFactory",
        factory_related_name="user",
        size=0
    )
    faculties = factory.RelatedFactory(
        factory="tests.apps.educational_institution.factories.FacultyFactory",
        factory_related_name="user",
        size=0
    )
    user_requests = factory.RelatedFactory(
        factory="tests.apps.services.factories.UserRequestFactory",
        factory_related_name="user",
        size=0
    )
    user_faculties = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.UserFacultyFactory",
        factory_related_name="user",
        size=0
    )

    class Meta:
        model = User
        exclude = (
            "role", "student", "user_request_reviews", "faculties", "user_requests", "user_faculties",
        )
        sqlalchemy_get_or_create = ("role_id",)


class OneTimeTokenFactory(BaseModelFactory):
    token_id = factory.Sequence(lambda x: x)
    token = factory.Faker("pystr", min_chars=1, max_chars=255)
    expires_at = factory.Faker("date_time")
    student_id = factory.SelfAttribute(attribute_name="student.student_id")
    student = factory.SubFactory(factory="tests.apps.users.factories.StudentFactory")

    class Meta:
        model = OneTimeToken
        exclude = ("student",)
        sqlalchemy_get_or_create = ("student_id",)


class StudentFactory(BaseModelFactory):
    student_id = factory.Sequence(lambda x: x)
    last_name = factory.Faker("last_name", min_chars=1, max_chars=50)
    first_name = factory.Faker("first_name", min_chars=1, max_chars=50)
    middle_name = factory.Faker("first_name", max_chars=50)
    telephone_number = factory.Faker("phone_number")
    gender = factory.Faker("pystr_format", string_format='?#{{random_letter}}', letters="ЧЖ")
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
    one_time_token = factory.RelatedFactory(
        factory="tests.apps.users.factories.OneTimeTokenFactory",
        factory_related_name="user_request",
        size=0
    )

    class Meta:
        model = Student
        exclude = ("course", "speciality", "user", "faculty", "one_time_token")
        sqlalchemy_get_or_create = (
            "course_id", "user_id", "faculty_id", "speciality_id"
        )


class UserFacultyFactory(BaseModelFactory):
    user_id = factory.SelfAttribute(attribute_name="user.user_id")
    faculty_id = factory.SelfAttribute(attribute_name="faculty.faculty_id")
    user = factory.SubFactory(factory=UserFactory)
    faculty = factory.SubFactory(factory=FacultyFactory)

    class Meta:
        model = UserFaculty
        exclude = ("user", "faculty")
        sqlalchemy_get_or_create = ("user_id", "faculty_id", "telephone_number")
