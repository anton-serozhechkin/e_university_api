import factory
from pytz import utc
from apps.authorization.models import Role, Action
from tests.bases import BaseModelFactory
from tests.apps.users.factories import UserFactory


class RoleFactory(BaseModelFactory):
    role_id = factory.Sequence(lambda x: x)
    role_name = factory.Faker("pystr", max_chars=50)
    created_at = factory.Faker("date_time", tzinfo=utc)
    updated_at = factory.Faker("date_time", tzinfo=utc)
    actions = factory.RelatedFactoryList(
        factory="tests.apps.authorization.factories.ActionFactory",
        factory_related_name="role",
        size=0
    )
    users = factory.RelatedFactoryList(
        factory=UserFactory,
        factory_related_name="role",
        size=0
    )

    class Meta:
        model = Role
        exclude = ("users", "actions")


class ActionFactory(BaseModelFactory):
    action_id = factory.Sequence(lambda x: x)
    action_name = factory.Faker("pystr", min_chars=1, max_chars=50)
    role_id = factory.SelfAttribute(attribute_name="roles.role_id")
    roles = factory.SubFactory(factory=RoleFactory)

    class Meta:
        model = Action
        exclude = ("roles",)
        sqlalchemy_get_or_create = ("role_id",)

