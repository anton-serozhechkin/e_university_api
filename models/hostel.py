from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)


metadata_obj = MetaData()


hostel = Table('hostel', metadata_obj,
          Column('hostel_id', Integer, primary_key=True),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('number', Integer),
          Column('name', VARCHAR(50)),
          Column('city', VARCHAR(50)),
          Column('street', VARCHAR(50)),
          Column('build', VARCHAR(5)),
          Column('commandant_id', Integer, ForeignKey("commandant.commandant.id")))
