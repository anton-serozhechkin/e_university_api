from typing import Dict, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Table

from apps.common.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)


class AsyncCRUDBase:
    def __init__(self, *, model: Type[ModelType]) -> None:
        self.model = model

    async def create(
        self,
        *,
        session: AsyncSession,
        data: Optional[Dict] = None,
        obj: Optional[CreateSchemaType] = None
    ) -> ModelType:
        data = data if data else {}
        obj_in_data = (
            jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False) if obj else {}
        )
        insert_statement = (
            insert(self.model).values(**data, **obj_in_data).returning(self.model)
        )
        statement = (
            select(self.model)
            .from_statement(insert_statement)
            .execution_options(populate_existing=True)
        )
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: ModelType = result.scalar_one()
        return data

    async def create_many(
        self, *, session: AsyncSession, objs: List[CreateSchemaType]
    ) -> Optional[List[ModelType]]:
        insert_statement = (
            insert(self.model)
            .values(
                [
                    jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False)
                    for obj in objs
                ]
            )
            .returning(self.model)
        )
        statement = (
            select(self.model)
            .from_statement(insert_statement)
            .execution_options(populate_existing=True)
        )
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: Union[List[ModelType], None] = result.scalars().all()
        return data

    async def read(
        self,
        *,
        session: AsyncSession,
        data: Optional[Dict] = None,
        obj: Optional[ReadSchemaType] = None
    ) -> Optional[ModelType]:
        data = data if data else {}
        obj_in_data = (
            jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False) if obj else {}
        )
        statement = select(self.model)
        model = self.model.c if isinstance(self.model, Table) else self.model
        for k, v in {**data, **obj_in_data}.items():
            statement = statement.where(getattr(model, k) == v)
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        response: Union[ModelType, None] = result.first()
        return (
            response if isinstance(self.model, Table) or not response else response[0]
        )

    async def update(
        self,
        *,
        session: AsyncSession,
        data: Optional[Dict] = None,
        obj: Union[Dict, UpdateSchemaType, None] = None
    ) -> Optional[ModelType]:
        obj = obj if obj else {}
        data = data if data else {}
        values = jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False)
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
            select(self.model)
            .from_statement(statement=update_statement)
            .execution_options(populate_existing=True)
        )
        result: ChunkedIteratorResult = await session.execute(statement=statement)
        await session.commit()
        data: Union[ModelType, None] = result.scalar_one_or_none()
        return data

    async def delete(
        self,
        *,
        session: AsyncSession,
        data: Optional[Dict] = None,
        obj: Optional[DeleteSchemaType] = None
    ) -> CursorResult:
        data = data if data else {}
        schema = (
            jsonable_encoder(obj=obj, exclude_unset=True, by_alias=False) if obj else {}
        )
        statement = delete(self.model)
        for k, v in {**data, **schema}.items():
            statement = statement.where(getattr(self.model, k) == v)
        result: CursorResult = await session.execute(statement=statement)
        await session.commit()
        return result

    async def list(
        self,
        *,
        session: AsyncSession,
        filters: Optional[Dict] = None  # TODO: Add dynamic filtering system
    ) -> List[
        Union[ReadSchemaType]
    ]:  # TODO: fix warning 'Union requires two or more type argumentsPylance'
        select_statement = select(self.model)
        if filters:
            select_statement = select_statement.filter_by(**filters)
        select_statement = select_statement.execution_options(populate_existing=True)
        result: ChunkedIteratorResult = await session.execute(
            statement=select_statement
        )
        if isinstance(self.model, Table):
            objects: List[Table] = result.all()
        else:
            objects: List[ReadSchemaType] = result.scalars().all()
        return objects
