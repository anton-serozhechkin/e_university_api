from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DateTime)


metadata_obj = MetaData()


hostel_list_view = Table('hostel_list_view', metadata_obj,
          Column('university_id', Integer),
          Column('hostel_id', Integer),
          Column('number', Integer),
          Column('name', VARCHAR(50)),
          Column('city', VARCHAR(50)),
          Column('street', VARCHAR(50)),
          Column('build', VARCHAR(50)),
          Column('commandant_id', Integer),
          Column('commandant_full_name', VARCHAR(255)))