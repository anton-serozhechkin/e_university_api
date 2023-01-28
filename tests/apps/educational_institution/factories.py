import factory

from apps.educational_institutions.models import (
    Course,
    Dean,
    Faculty,
    Rector,
    Speciality,
    University,
)
from tests.bases import BaseModelFactory


class RectorFactory(BaseModelFactory):
    rector_id = factory.Sequence(lambda x: x)
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    university = factory.RelatedFactoryList(
        factory="tests.apps.educational_institution.factories.UniversityFactory",
        factory_related_name="rector",
        size=0,
    )

    class Meta:
        model = Rector
        exclude = ("university",)


class UniversityFactory(BaseModelFactory):
    university_id = factory.Sequence(lambda x: x)
    university_name = factory.Faker("pystr", max_chars=255, min_chars=10)
    short_university_name = factory.Faker("pystr", max_chars=50, min_chars=3)
    city = factory.Faker("pystr", max_chars=255, min_chars=4)
    logo = factory.Faker("pystr", max_chars=255)
    rector_id = factory.SelfAttribute(attribute_name="rector.rector_id")
    rector = factory.SubFactory(
        factory="tests.apps.educational_institution.factories.RectorFactory"
    )
    faculties = factory.RelatedFactoryList(
        factory="tests.apps.educational_institution.factories.FacultyFactory",
        factory_related_name="university",
        size=0,
    )
    hostels = factory.RelatedFactoryList(
        factory="tests.apps.hostels.factories.HostelFactory",
        factory_related_name="university",
        size=0,
    )
    requisites = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.RequisitesFactory",
        factory_related_name="university",
        size=0,
    )
    user_request_reviews = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestReviewFactory",
        factory_related_name="university",
        size=0,
    )
    user_requests = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestFactory",
        factory_related_name="university",
        size=0,
    )
    service_document = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.ServiceDocumentFactory",
        factory_related_name="university",
        size=0,
    )

    class Meta:
        model = University
        exclude = (
            "rector",
            "faculties",
            "hostels",
            "requisites",
            "user_request_reviews",
            "user_requests",
            "service_document",
        )
        sqlalchemy_get_or_create = ("rector_id",)


class FacultyFactory(BaseModelFactory):
    faculty_id = factory.Sequence(lambda x: x)
    name = factory.Faker("pystr", max_chars=255, min_chars=3)
    shortname = factory.Faker("pystr", max_chars=20, min_chars=3)
    main_email = factory.Faker("pystr", max_chars=50)
    dean_id = factory.SelfAttribute(attribute_name="dean.dean_id")
    dean = factory.SubFactory(
        factory="tests.apps.educational_institution.factories.DeanFactory"
    )
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    speciality = factory.RelatedFactoryList(
        factory="tests.apps.educational_institution.factories.SpecialityFactory",
        factory_related_name="Faculty",
        size=0,
    )
    students = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.StudentFactory",
        factory_related_name="Faculty",
        size=0,
    )
    users = factory.RelatedFactoryList(
        factory="tests.apps.users.factories.UserFacultyFactory",
        factory_related_name="Faculty",
        size=0,
    )
    user_requests = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestFactory",
        factory_related_name="Faculty",
        size=0,
    )

    class Meta:
        model = Faculty
        exclude = (
            "dean",
            "university",
            "speciality",
            "students",
            "users",
            "user_requests",
        )
        sqlalchemy_get_or_create = ("dean_id", "university_id")


class SpecialityFactory(BaseModelFactory):
    speciality_id = factory.Sequence(lambda x: x)
    code = factory.Faker("pyint", min_value=1)
    name = factory.Faker("pystr", min_chars=4, max_chars=255)
    faculty_id = factory.SelfAttribute(attribute_name="faculties.faculty_id")
    faculties = factory.SubFactory(factory=FacultyFactory)

    class Meta:
        model = Speciality
        exclude = ("faculties",)
        sqlalchemy_get_or_create = ("faculty_id",)


class DeanFactory(BaseModelFactory):
    dean_id = factory.Sequence(lambda x: x)
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    faculty = factory.RelatedFactoryList(
        factory="tests.apps.educational_institution.factories.FacultyFactory",
        factory_related_name="dean",
        size=0,
    )

    class Meta:
        model = Dean
        exclude = ("faculty",)


class CourseFactory(BaseModelFactory):
    course_id = factory.Sequence(lambda x: x)
    value = factory.Faker("pyint", min_value=1, max_value=6)

    class Meta:
        model = Course
