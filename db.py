from settings import Settings

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

database = databases.Database(Settings.POSTGRES_DSN)

engine = sqlalchemy.create_engine(Settings.POSTGRES_DSN)

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = sqlalchemy.MetaData(naming_convention=convention)

metadata.create_all(engine)
