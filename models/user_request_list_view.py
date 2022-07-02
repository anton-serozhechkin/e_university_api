
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DateTime)


metadata_obj = MetaData()


user_request_list_view = Table('user_request_list_view', metadata_obj,
          Column('university_id', Integer),
          Column('user_id', Integer),
          Column('user_request_id', Integer),
          Column('service_name', VARCHAR(255)),
          Column('status_name', VARCHAR(50)),
          Column('date_created', DateTime))
