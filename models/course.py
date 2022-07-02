from sqlalchemy import (MetaData, Column, Table, Integer)


metadata_obj = MetaData()


course = Table('course', metadata_obj,
          Column('course_id', Integer, primary_key=True),
          Column('value', Integer))
