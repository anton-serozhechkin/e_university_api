from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, FLOAT)


metadata_obj = MetaData()


hostel = Table('hostel', metadata_obj,
          Column('hostel_id', Integer, primary_key=True),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('number', Integer),
          Column('name', VARCHAR(100)),
          Column('city', VARCHAR(100)),
          Column('street', VARCHAR(100)),
          Column('build', VARCHAR(10)),
          Column('month_price', FLOAT),
          Column('commandant_id', Integer, ForeignKey("commandant.commandant.id")))


commandant = Table('commandant', metadata_obj,
          Column('commandant_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)),
          Column('telephone_number', VARCHAR(50)))


bed_places = Table('bed_places', metadata_obj,
          Column('bed_place_id', Integer, primary_key=True),
          Column('bed_place_name', VARCHAR(50)))

