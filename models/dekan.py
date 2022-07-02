from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


dekan = Table('dekan', metadata_obj,
          Column('dekan_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)))
