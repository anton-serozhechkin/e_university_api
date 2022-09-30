import databases
import sqlalchemy 
from settings import ProjectSettings

DATABASE_URL = ProjectSettings.POSTGRES_DSN

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
