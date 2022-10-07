# from sqlalchemy import (Column, INTEGER, VARCHAR)
#
# from db import Base
#
#
# class StudentsListView(Base):
#     __tablename__ = 'students_list_view'
#
#     student_id = Column(INTEGER)
#     student_full_name = Column(VARCHAR(length=255))
#     telephone_number = Column(INTEGER)
#     user_id = Column(INTEGER)
#     university_id = Column(INTEGER)
#     faculty_id = Column(INTEGER)
#     speciality_id = Column(INTEGER)
#     course_id = Column(INTEGER)
#     gender = Column(VARCHAR(length=1))
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(student_id="{self.student_id}",student_full_name="{self.student_full_name}",telephone_number="{self.telephone_number}",user_id="{self.user_id}",university_id="{self.university_id}",faculty_id="{self.faculty_id}",speciality_id="{self.speciality_id}",course_id="{self.course_id}",gender="{self.gender}")'
#
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


students_list_view = Table('students_list_view', metadata_obj,
          Column('student_id', Integer),
          Column('student_full_name', VARCHAR(255)),
          Column('telephone_number', Integer),
          Column('user_id', Integer),
          Column('university_id', Integer),
          Column('faculty_id', Integer),
          Column('speciality_id', Integer),
          Column('course_id', Integer),
          Column('gender',VARCHAR(1)))