from sqlalchemy import (MetaData, Column, Table, Integer, ForeignKey, VARCHAR)


metadata_obj = MetaData()


speciality = Table('speciality', metadata_obj,
          Column('speciality_id', Integer, primary_key=True),
          Column('code', Integer),
          Column('name', VARCHAR(255)),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id"), nullable=False))
