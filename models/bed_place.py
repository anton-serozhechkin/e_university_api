from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)

metadata_obj = MetaData()

bed_place = Table('bed_place', metadata_obj,
          Column('bed_place_id', Integer, primary_key=True),
          Column('bed_place_name', VARCHAR(50)))
