import factory
from apps.hostel.models import BedPlace, Commandant, Hostel
from tests.bases import BaseModelFactory
from tests.apps.educational_institution.factories import UniversityFactory


class BedPlaceFactory(BaseModelFactory):
    bed_place_id = factory.Sequence(lambda x: x)
    bed_place_name = factory.Faker("name")

    user_request_review = factory.RelatedFactoryList(
        factory="tests.apps.services.factories.UserRequestReviewFactory",
        factory_related_name="bed_place",
        size=0,
    )

    class Meta:
        model = BedPlace
        exclude = ("user_request_review",)


class CommandantFactory(BaseModelFactory):
    commandant_id = factory.Sequence(lambda x: x)
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    telephone_number = factory.Faker("phone_number")

    hostel = factory.RelatedFactoryList(
        factory="tests.apps.hostel.factories.HostelFactory",
        factory_related_name="commandant",
        size=0,
    )

    class Meta:
        model = Commandant
        exclude = ("hostel",)
        sqlalchemy_get_or_create = ("telephone_number",)


class HostelFactory(BaseModelFactory):
    hostel_id = factory.Sequence(lambda x: x)
    number = factory.Faker("pyint", min_value=1, max_value=100)
    name = factory.Faker("pystr", max_chars=100, min_chars=2)
    city = factory.Faker("pystr", max_chars=100, min_chars=10)
    street = factory.Faker("pystr", max_chars=100, min_chars=10)
    build = factory.Faker("pystr", max_chars=10, min_chars=1)
    month_price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    commandant_id = factory.SelfAttribute(attribute_name="commandant.commandant_id")
    university_id = factory.SelfAttribute(attribute_name="university.university_id")
    university = factory.SubFactory(factory=UniversityFactory)
    commandant = factory.SubFactory(factory=CommandantFactory)

    class Meta:
        model = Hostel
        exclude = ("university", "commandant")
        sqlalchemy_get_or_create = ("university_id", "commandant_id")
