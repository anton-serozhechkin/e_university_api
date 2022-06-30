from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)

metadata_obj = MetaData()

dekan = Table('rector', metadata_obj,
          Column('rector_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)))