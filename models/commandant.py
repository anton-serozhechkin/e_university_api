from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


commandant = Table('commandant', metadata_obj,
          Column('commandant_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)),
          Column('telephone_number', VARCHAR(255)))