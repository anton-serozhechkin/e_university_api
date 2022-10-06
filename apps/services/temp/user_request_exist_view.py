from sqlalchemy import (MetaData, Column, Table, Integer, JSON)


metadata_obj = MetaData()


user_request_exist_view = Table('user_request_exist_view', metadata_obj,
          Column('user_request_id', Integer),
          Column('user_id', Integer),
          Column('faculty_id', Integer),
          Column('university_id', Integer),
          Column('service_id', Integer),
          Column('status', JSON))
