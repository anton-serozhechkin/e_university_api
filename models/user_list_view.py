from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, TIMESTAMP)

metadata_obj = MetaData()

user_list_view = Table('user_list_view', metadata_obj,
          Column('user_id', Integer),
          Column('login', VARCHAR(50)),
          Column('last_visit', TIMESTAMP),
          Column('email', VARCHAR(50)),
          Column('role_id', Integer),
          Column('role_name', VARCHAR(50)),
          Column('university_id', Integer),
          Column('faculty_name', VARCHAR(255)),
          Column('faculty_id', Integer))
