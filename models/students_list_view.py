from ast import Str
from sqlalchemy import (MetaData, Column, Table, Integer, String, VARCHAR) 


metadata_obj = MetaData()


students_list_view = Table('students_list_view', metadata_obj,
          Column('student_id', Integer),
          Column('student_full_name', VARCHAR(255)),
          Column('telephone_number', String),
          Column('user_id', Integer),
          Column('university_id', Integer),
          Column('faculty_id', Integer),
          Column('speciality_id', Integer),
          Column('course_id', Integer),
          Column('gender',VARCHAR(1)))