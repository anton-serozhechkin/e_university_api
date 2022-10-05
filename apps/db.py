import os

import databases
import sqlalchemy 


DATABASE_URL = os.getenv("DATABASE_URL", None)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
