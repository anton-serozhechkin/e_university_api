from settings import Settings

import databases
import sqlalchemy 


database = databases.Database(Settings.POSTGRES_DSN)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(Settings.POSTGRES_DSN)

metadata.create_all(engine)
