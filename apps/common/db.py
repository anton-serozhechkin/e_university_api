from settings import Settings

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

database = databases.Database(Settings.POSTGRES_DSN)

engine = sqlalchemy.create_engine(Settings.POSTGRES_DSN)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = sqlalchemy.MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

metadata.create_all(engine)
