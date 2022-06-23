from datetime import timedelta
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)


metadata_obj = MetaData()

user_request = Table('user_request', metadata_obj,
          Column('user_id', Integer),
          Column('service_id', VARCHAR(255)),
          Column('date_created', timedelta),
          Column('user_request_id', Integer, primary_key=True),
          Column('status_id', Integer, ForeignKey("status.status_id")),
          Column('remarks', VARCHAR(255)),
          Column('reviever_id', Integer),
          Column('date_review', timedelta))
