from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)


metadata_obj = MetaData()


student = Table('student', metadata_obj,
          Column('student_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)),
          Column('telephone_number', Integer),
          Column('', VARCHAR(1)),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id")),
          Column('course_id', Integer, ForeignKey("course.course_id")),
          Column('speciality_id', Integer, ForeignKey("speciality.speciality_id")),
          Column('user_id', Integer, ForeignKey("user.user_id"), nullable=True))
