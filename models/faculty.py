from sqlalchemy import *
from models.university import university

metadata_obj = MetaData()

faculty = Table('faculty', metadata_obj,
    Column('faculty_id', Integer, primary_key = True),
    Column('name', VARCHAR(255), nullable=False),
    Column('shortname', VARCHAR(20)),
    Column('main_email', VARCHAR(50)),
    Column('hostel_email', VARCHAR(50)))
    #Column('university_id', Integer, ForeignKey(university.university_id)))
