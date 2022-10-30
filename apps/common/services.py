import uuid
from typing import Type, TypeVar, Union, List, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult, FilterResult, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Table

from apps.common.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class AsyncCRUDBase:
    def __init__(self, *, model: Type[ModelType]):
        self.model = model

    async def create(self, *, session: AsyncSession, obj: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False)
        insert_statement = insert(self.model).values(**obj_in_data).returning(self.model)
        statement = select(self.model).from_statement(insert_statement).execution_options(populate_existing=True)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: ModelType = result.scalar_one()
        return data

    async def create_mod(self, *, session: AsyncSession, data: Dict = dict, schema: Union[CreateSchemaType, None] = None):
        obj_in_data = jsonable_encoder(obj=schema, exclude_unset=True, by_alias=False) if schema else {}
        insert_statement = insert(self.model).values(**data, **obj_in_data).returning(self.model)
        statement = select(self.model).from_statement(insert_statement).execution_options(populate_existing=True)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: ModelType = result.scalar_one()
        return data

    async def create_many(self, *, session: AsyncSession, objs: List[CreateSchemaType]) -> Union[List[ModelType], None]:
        insert_statement = (
            insert(self.model)
            .values([jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False) for obj in objs])
            .returning(self.model)
        )
        statement = select(self.model).from_statement(insert_statement).execution_options(populate_existing=True)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: Union[List[ModelType], None] = result.scalars().all()
        return data

    async def read(self, *, session: AsyncSession, id: Union[str, uuid.UUID]) -> Union[ModelType, None]:
        statement = select(self.model).where(self.model.id == id)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        data: Union[ModelType, None] = result.scalar_one_or_none()
        return data

    async def read_mod(self, *, session: AsyncSession, data: Dict = dict, schema: Union[ReadSchemaType, None] = None):
        obj_in_data = jsonable_encoder(obj=schema, exclude_unset=True, by_alias=False) if schema else {}
        where_dict = {**data, **obj_in_data}
        statement = select(self.model)
        model = self.model.c if isinstance(self.model, Table) else self.model
        for k, v in where_dict.items():
            statement = statement.where(getattr(model, k) == v)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        response: Union[ModelType, None] = result.first()
        return response if isinstance(self.model, Table) else response[0]

    async def update(self, *, session: AsyncSession, id: Union[str, uuid.UUID], obj: UpdateSchemaType) -> Union[ModelType, None]:
        values = jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False)
        update_statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(**values)
            .returning(self.model)
            .execution_options(synchronize_session="fetch")
        )
        statement = (
            select(self.model).from_statement(statement=update_statement).execution_options(populate_existing=True)
        )
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: Union[ModelType, None] = result.scalar_one_or_none()
        return data

    async def update_mod(self, *, session: AsyncSession, data: Dict = dict, obj: Union[Dict, UpdateSchemaType] = dict) -> Union[ModelType, None]:
        values = obj if isinstance(obj, Dict) else jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False)
        where_expr = []
        for k, v in data.items():
            where_expr.append(getattr(self.model, k) == v)
        update_statement = (
            update(self.model)
            .where(and_(*where_expr))
            .values(**values)
            .returning(self.model)
            .execution_options(synchronize_session="fetch")
        )
        statement = (
            select(self.model).from_statement(statement=update_statement).execution_options(populate_existing=True)
        )
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: Union[ModelType, None] = result.scalar_one_or_none()
        return data

    async def delete(self, *, session: AsyncSession, id: Union[str, uuid.UUID]) -> CursorResult:
        delete_statement = delete(self.model).where(self.model.id == id)
        result: CursorResult = await session.execute(statement=delete_statement)
        await session.commit()
        return result

    async def list(
        self,
        *,
        session: AsyncSession,
        filters: Union[Dict, None] = None  # TODO: Add dynamic filtering system
    ) -> List[Union[ReadSchemaType]]:
        select_statement = select(self.model)
        if filters:
            select_statement = select_statement.filter_by(**filters)
        select_statement = select_statement.execution_options(populate_existing=True)

        result: ChunkedIteratorResult = await session.execute(statement=select_statement)
        if isinstance(self.model, Table):
            objects: List[Table] = result.all()
        else:
            objects: List[ReadSchemaType] = result.scalars().all()
        return objects
