# from sqlalchemy import (Column, INTEGER, VARCHAR)
#
# from db import Base
#
#
# class HostelListView(Base):
#     __tablename__ = 'hostel_list_view'
#
#     university_id = Column(INTEGER)
#     hostel_id = Column(INTEGER)
#     number = Column(INTEGER)
#     name = Column(VARCHAR(length=100))
#     city = Column(VARCHAR(length=100))
#     street = Column(VARCHAR(length=100))
#     build = Column(VARCHAR(length=10))
#     commandant_id = Column(INTEGER)
#     commandant_full_name = Column(VARCHAR(length=255))
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(university_id="{self.university_id}",hostel_id="{self.hostel_id}",number="{self.number}", ' \
#                f'name="{self.name}",city="{self.city}",street="{self.street}", build="{self.build}",commandant_id="{self.commandant_id}",' \
#                f'commandant_full_name="{self.commandant_full_name}")'
#
#
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
          Column('commandant_full_name', VARCHAR(255)))