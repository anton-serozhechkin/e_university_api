# from sqlalchemy import (Column, INTEGER, VARCHAR, DATETIME, PrimaryKeyConstraint)
#
# from db import Base
#
#
# class UserRequestBookingHostelView(Base):
#     __tablename__ = "user_request_booking_hostel_view"
#
#     full_name = Column(VARCHAR(length=255))
#     user_id = Column(INTEGER)
#     faculty_name = Column(VARCHAR(length=255))
#     university_id = Column(INTEGER)
#     short_university_name = Column(VARCHAR(length=50))
#     rector_full_name = Column(VARCHAR(length=255))
#     speciality_code = Column(INTEGER)
#     speciality_name = Column(VARCHAR(length=255))
#     course = Column(INTEGER)
#     educ_level = Column(VARCHAR(length=1))
#     date_today = Column(DATETIME)
#     start_year = Column(INTEGER)
#     finish_year = Column(INTEGER)
#     gender = Column(VARCHAR(length=1))
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(full_name="{self.full_name}", user_id="{self.user_id}", faculty_name="{self.faculty_name}", university_id="{self.university_id}", ' \
#                f'short_university_name="{self.short_university_name}", rector_full_name="{self.rector_full_name}", speciality_code="{self.speciality_code}", ' \
#                f'speciality_name="{self.speciality_name}", course="{self.course}", educ_level="{self.educ_level}", date_today="{self.date_today}", start_year="{self.start_year}", ' \
#                f'finish_year="{self.finish_year}", gender="{self.gender}")'
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DATETIME)


metadata_obj = MetaData()


user_request_booking_hostel_view = Table('user_request_booking_hostel_view', metadata_obj,
          Column('full_name', VARCHAR(255)),
          Column('user_id', Integer),
          Column('faculty_name', VARCHAR(255)),
          Column('university_id', Integer),
          Column('short_university_name', VARCHAR(50)),
          Column('rector_full_name', VARCHAR(255)),
          Column('speciality_code', Integer),
          Column('speciality_name', VARCHAR(255)),
          Column('course', Integer),
          Column('educ_level', VARCHAR(1)),
          Column('date_today', DATETIME),
          Column('start_year', Integer),
          Column('finish_year', Integer),
          Column('gender', VARCHAR(1)))