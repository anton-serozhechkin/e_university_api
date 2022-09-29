import os
import databases
import sqlalchemy 
from settings.settings import Settings

DATABASE_URL = Settings.POSTGRES_DSN

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
