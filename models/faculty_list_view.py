# from sqlalchemy import (Column, INTEGER, VARCHAR)
#
# from db import Base
#
#
# class FacultyListView(Base):
#     __tablename__ = 'faculty_list_view'
#
#     faculty_id = Column(INTEGER)
#     name = Column(VARCHAR(length=255))
#     shortname = Column(VARCHAR(length=20))
#     main_email = Column(VARCHAR(length=50))
#     university_id = Column(INTEGER)
#     dekan_id = Column(INTEGER)
#     dekan_full_name = Column(VARCHAR(length=255))
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(faculty_id="{self.faculty_id}",name="{self.name}",shortname="{self.shortname}",' \
#                f'main_email="{self.main_email}", university_id="{self.university_id}", dekan_id="{self.dekan_id}",' \
#                f'dekan_full_name="{self.dekan_full_name}")'
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


faculty_list_view = Table('faculty_list_view', metadata_obj,
          Column('faculty_id', Integer),
          Column('name', VARCHAR(255)),
          Column('shortname', VARCHAR(20)),
          Column('main_email', VARCHAR(50)),
          Column('university_id', Integer),
          Column('dekan_id', Integer),
          Column('decan_full_name', VARCHAR(255)))