from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


service = Table('service', metadata_obj,
          Column('service_id', Integer, primary_key=True),
          Column('service_name', VARCHAR(255)))
