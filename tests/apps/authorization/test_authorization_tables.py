from apps.authorization.models import Role, Action
from tests.apps.authorization.factories import RoleFactory, ActionFactory
from tests.bases import BaseModelFactory


class TestRole:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=RoleFactory, model=Role)

    def test__repr__(self) -> None:
        obj: Role = RoleFactory()
        expected_result = (
            f'{obj.__class__.__name__}(role_id="{obj.role_id}",'
            f' role_name="{obj.role_name}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestAction:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=ActionFactory, model=Action)

    def test__repr__(self) -> None:
        obj: Action = ActionFactory()
        expected_result = (
            f'{obj.__class__.__name__}(action_id="{obj.action_id}",'
            f' action_name="{obj.action_name}",role_id="{obj.role_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result
