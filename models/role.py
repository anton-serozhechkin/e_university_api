from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)

metadata_obj = MetaData()

role = Table('role', metadata_obj,
          Column('role_id', Integer, primary_key=True),
          Column('role_name', VARCHAR(50)))
