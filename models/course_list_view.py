from sqlalchemy import (MetaData, Column, Table, Integer)


metadata_obj = MetaData()


course_list_view = Table('course_list_view', metadata_obj,
          Column('course_id', Integer),
          Column('course_number', Integer))
