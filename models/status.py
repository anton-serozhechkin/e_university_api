from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)

metadata_obj = MetaData()

status = Table('status', metadata_obj,
          Column('status_id', Integer, primary_key=True),
          Column('status_name', VARCHAR(255)))
