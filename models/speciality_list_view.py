# from sqlalchemy import (Column, INTEGER, JSON)
#
# from db import Base
#
#
# class SpecialityListView(Base):
#     __tablename__ = "speciality_list_view"
#
#     faculty_id = Column(INTEGER)
#     speciality_id = Column(INTEGER)
#     university_id = Column(INTEGER)
#     speciality_info = Column(JSON)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(faculty_id="{self.faculty_id}",speciality_id="{self.speciality_id}",university_id="{self.university_id}",speciality_info="{self.speciality_info}")'
from sqlalchemy import (MetaData, Column, Table, Integer, JSON)


metadata_obj = MetaData()


speciality_list_view = Table('speciality_list_view', metadata_obj,
          Column('faculty_id', Integer),
          Column('speciality_id', Integer),
          Column('university_id', Integer),
          Column('speciality_info', JSON))