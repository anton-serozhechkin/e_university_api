from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


hostel_list_view = Table('hostel_list_view', metadata_obj,
          Column('university_id', Integer),
          Column('hostel_id', Integer),
          Column('number', Integer),
          Column('name', VARCHAR(100)),
          Column('city', VARCHAR(100)),
          Column('street', VARCHAR(100)),
          Column('build', VARCHAR(10)),
          Column('commandant_id', Integer),
          Column('first_name', VARCHAR(255)),
          Column('last_name', VARCHAR(255)),
          Column('middle_name', VARCHAR(255)))
