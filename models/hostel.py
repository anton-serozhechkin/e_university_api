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
