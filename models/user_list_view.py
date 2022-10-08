from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, TIMESTAMP, JSON, BOOLEAN)


metadata_obj = MetaData()


user_list_view = Table('user_list_view', metadata_obj,
          Column('user_id', Integer),
          Column('login', VARCHAR(50)),
          Column('last_visit', TIMESTAMP),
          Column('email', VARCHAR(50)),
          Column('role', JSON),
          Column('is_active', BOOLEAN),
          Column('university_id', Integer),
          Column('faculties', JSON))