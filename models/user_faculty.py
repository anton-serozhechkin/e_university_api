from sqlalchemy import (MetaData, Column, Table, Integer, ForeignKey)

metadata_obj = MetaData()

user_faculty = Table('user_faculty', metadata_obj,
          Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False, primary_key=True),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id"), nullable=False, primary_key=True))
