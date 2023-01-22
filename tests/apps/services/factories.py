from pytz import utc
import factory
from apps.services.models import Service, UserRequest, Status, Requisites, UserRequestReview, UserDocument, ServiceDocument
from tests.bases import BaseModelFactory
from tests.apps.educational_institution.factories import UniversityFactory, FacultyFactory
from tests.apps.hostel.factories import BedPlaceFactory, HostelFactory
from tests.apps.users.factories import UserFactory


class ServiceFactory(BaseModelFactory):
    service_id = factory.Sequence(lambda x: x)
    service_name = factory.Faker("pystr", min_chars=3, max_chars=255)

    requisites = factory.RelatedFactory(
        factory="tests.apps.services.factories.RequisitesFactory",
        factory_related_name="service",
        size=0
    )
    user_requests = factory.RelatedFactory(
        factory="tests.apps.services.factories.UserRequestsFactory",
        factory_related_name="service",
        size=0
    )
    service_document = factory.RelatedFactory(
        factory="tests.apps.services.factories.ServiceDocumentFactory",
        factory_related_name="service",
        size=0
    )

    class Meta:
        model = Service
        exclude = ("service_document", "user_requests", "requisites")


class UserRequestFactory(BaseModelFactory):
    user_request_id = factory.Sequence(lambda x: x)
    comment = factory.Faker("pystr", max_chars=255)
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    user_id = factory.SelfAttribute(attribute_name="user.user_id")
    user = factory.SubFactory(factory="tests.apps.users.factories.UserFaculty")
    service_id = factory.SelfAttribute(attribute_name="service.service_id")
    service = factory.SubFactory(factory=ServiceFactory)
    faculty_id = factory.SelfAttribute(attribute_name="faculty.faculty_id")
    faculty = factory.SubFactory(factory=FacultyFactory)
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    status_id = factory.SelfAttribute(attribute_name="status.status_id")
    status = factory.SubFactory(factory="tests.apps.services.factories.StatusFactory")
    user_documents = factory.RelatedFactory(
        factory="tests.apps.services.factories.UserDocumentFactory",
        factory_related_name="user_request",
        size=0
    )
    user_request_review = factory.RelatedFactory(
        factory="tests.apps.services.factories.UserRequestReviewFactory",
        factory_related_name="user_request",
        size=0
    )

    class Meta:
        model = UserRequest
        exclude = (
            "user_documents", "user_request_review", "user", "service", "faculty", "university", "status")
        sqlalchemy_get_or_create = (
            "user_id", "service_id", "faculty_id", "university_id", "status_id"
        )


class StatusFactory(BaseModelFactory):
    status_id = factory.Sequence(lambda x: x)
    status_name = factory.Faker("pystr", min_chars=1, max_chars=50)
    user_requests = factory.RelatedFactory(
        factory=UserRequestFactory,
        factory_related_name="status",
        size=0
    )

    class Meta:
        model = Status
        exclude = ("user_requests",)
        sqlalchemy_get_or_create = ("status_name",)


class RequisitesFactories(BaseModelFactory):
    requisites_id = factory.Sequence(lambda x: x)
    iban = factory.Faker("pystr", max_chars=100)
    organisation_code = factory.Faker("pystr", max_chars=50)
    payment_recognition = factory.Faker("pystr", max_chars=255)
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    service_id = factory.SelfAttribute(attribute_name="service.service_id")
    service = factory.SubFactory(factory=ServiceFactory)
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)

    class Meta:
        model = Requisites
        exclude = ("university", "service")
        sqlalchemy_get_or_create = ("university_id", "service_id")


class UserRequestReviewFactory(BaseModelFactory):
    user_request_review_id = factory.Sequence(lambda x: x)
    room_number = factory.Faker("pyint")
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    start_accommodation_date = factory.Faker("date")
    end_accommodation_date = factory.Faker("date")
    total_sum = factory.Faker("pydecimal", left_digits=7, right_digits=2, positive=True)
    payment_deadline_date = factory.Faker("date")
    remark = factory.Faker("pystr", max_chars=255)
    bed_place_id = factory.SelfAttribute(attribute_name="bed_place.bed_place_id")
    bed_place = factory.SubFactory(factory=BedPlaceFactory)
    reviewer = factory.SelfAttribute(attribute_name="reviewer_user.user_id")
    reviewer_user = factory.SubFactory(factory=UserFactory)
    hostel_id = factory.SelfAttribute(attribute_name="hostel.hostel_id")
    hostel = factory.SubFactory(factory=HostelFactory)
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    user_request_id = factory.SelfAttribute(attribute_name="user_request.user_request_id")
    user_request = factory.SubFactory(factory=UserRequestFactory)

    class Meta:
        model = UserRequestReview
        exclude = (
            "bed_place",
            "reviewer_user",
            "hostel",
            "university",
            "user_request",
        )
        sqlalchemy_get_or_create = (
            "bed_place_id", "reviewer", "hostel_id", "university_id", "user_request_id")


class UserDocumentFactory(BaseModelFactory):
    user_document_id = factory.Sequence(lambda x: x)
    name = factory.Faker("pystr", min_chars=1, max_chars=255)
    content = factory.Faker("pystr", min_chars=1, max_chars=255)
    user_request_id = factory.SelfAttribute(attribute_name="user_request.user_request_id")
    user_request = factory.SubFactory(factory=UserRequestFactory)
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)

    class Meta:
        model = UserDocument
        exclude = ("user_request",)
        sqlalchemy_get_or_create = ("user_request_id",)


class ServiceDocumentFactory(BaseModelFactory):
    service_document_id = factory.Sequence(lambda x: x)
    service_id = factory.SelfAttribute(attribute_name="service.service_id")
    service = factory.SubFactory(factory=ServiceFactory)
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    documents = factory.Faker("pystr", min_chars=1)

    class Meta:
        model = ServiceDocument
        exclude = ("service", "university")
        sqlalchemy_get_or_create = ("service_id", "university_id")
