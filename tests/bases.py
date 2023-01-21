import datetime
from typing import Any, Dict, List, Type
import typing
import random

from pydantic_factories import AsyncPersistenceProtocol, ModelFactory, PostGenerated
from pytz import utc
import factory
from apps.common.db import Base, async_session_factory
from apps.common.services import AsyncCRUDBase, CreateSchemaType, ModelType


starting_seq_num = 0


class AsyncPersistenceHandler(AsyncPersistenceProtocol):
    def __init__(self, model: Type[Base]) -> None:
        self._model = model
        self._service = AsyncCRUDBase(model=self._model)

    async def save(self, data: CreateSchemaType) -> ModelType:
        async with async_session_factory() as db_session:
            async with db_session.begin():
                return await self._service.create(session=db_session, obj=data)

    async def save_many(self, data: List[CreateSchemaType]) -> List[ModelType]:
        async with async_session_factory() as db_session:
            async with db_session.begin():
                return await self._service.create_many(session=db_session, objs=data)


class BaseRawFactory(ModelFactory):
    @classmethod
    def get_mock_value(cls, field_type: Any) -> Any:
        type_name = str(field_type.__name__)
        if type_name == "Email":
            return cls.get_faker().email()
        return super().get_mock_value(field_type)


def generate_dt(name: str, values: Dict[str, Any]) -> datetime.datetime:
    result = datetime.datetime.now(tz=utc)
    if name == "updated_at":
        result = values["created_at"]
    return result


class BaseFactory(BaseRawFactory):
    created_at: datetime.datetime = PostGenerated(fn=generate_dt)
    updated_at: datetime.datetime = PostGenerated(fn=generate_dt)


class BaseModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Change RuntimeError to help with factory set up."""
        if cls._meta.sqlalchemy_session is None:
            raise RuntimeError(
                f"Register {cls.__name__} factory inside conftest.py in set_session_for_factories fixture declaration."
            )
        return super()._create(model_class=model_class, *args, **kwargs)

    @staticmethod
    def check_factory(factory_class: typing.Type["BaseModelFactory"], model: typing.Type[Base]) -> None:
        """Test that factory creates successfully."""
        obj = factory_class()
        size = random.randint(2, 3)
        objs = factory_class.create_batch(size=size)

        assert isinstance(obj, model)
        assert size == len(objs)
        for i in objs:
            assert isinstance(i, model)

    # @classmethod
    # def _setup_next_sequence(cls):
    #     return starting_seq_num

