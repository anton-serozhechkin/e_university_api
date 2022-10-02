from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, 
                        BOOLEAN, TIMESTAMP)

metadata_obj = MetaData()

user = Table('user', metadata_obj,
          Column('user_id', Integer, primary_key=True),
          Column('login', VARCHAR(50)),
          Column('password', VARCHAR(50)),
          Column('last_visit', TIMESTAMP),
          Column('email', VARCHAR(100)), 
          Column('is_active', BOOLEAN),
          Column('role_id', Integer, ForeignKey("role.role_id"), nullable=True))


one_time_token = Table('one_time_token', metadata_obj,
          Column('student_id', Integer, ForeignKey("student.student_id"), nullable=False),
          Column('token_id', Integer, primary_key=True),
          Column('token', VARCHAR(255), nullable=False),
          Column('expires', TIMESTAMP, nullable=False))


student = Table('student', metadata_obj,
          Column('student_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)),
          Column('telephone_number', Integer),
          Column('gender', VARCHAR(1)),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id")),
          Column('course_id', Integer, ForeignKey("course.course_id")),
          Column('speciality_id', Integer, ForeignKey("speciality.speciality_id")),
          Column('user_id', Integer, ForeignKey("user.user_id"), nullable=True))


user_faculty = Table('user_faculty', metadata_obj,
          Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False, primary_key=True),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id"), nullable=False, primary_key=True))
