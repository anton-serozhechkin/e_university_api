from settings import Settings

import re
import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_mixin, declared_attr

database = databases.Database(Settings.POSTGRES_DSN)


@declarative_mixin
class TableNameMixin:
    """Mixin for rewrite table name magic method."""

    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.pattern.sub("_", cls.__name__).lower()


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",  # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # UniqueConstraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # ForeignKey
    "pk": "pk_%(table_name)s",  # PrimaryKey
}
Base = declarative_base(cls=TableNameMixin, metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION))

engine = sqlalchemy.create_engine(Settings.POSTGRES_DSN)

metadata = sqlalchemy.MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

metadata.create_all(engine)
