from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)

from e_university_api.models import faculty 
from e_university_api.models import user

metadata_obj = MetaData()

student = Table('student', metadata_obj,
          Column('student_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)),
          Column('telephone_number', Integer),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id")),
          Column('user_id', Integer, ForeignKey("user.user_id"), nullable=True))
