import databases
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from settings import Settings

database = databases.Database(str(Settings.POSTGRES_DSN))


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

Base = declarative_base(
    metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
)
async_engine = create_async_engine(
    url=Settings.POSTGRES_DSN_ASYNC, echo=Settings.POSTGRES_ECHO
)
engine = create_engine(url=Settings.POSTGRES_DSN, echo=Settings.POSTGRES_ECHO)
async_session_factory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
session_factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
