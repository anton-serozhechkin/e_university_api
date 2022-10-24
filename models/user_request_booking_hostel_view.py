from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DATETIME)


metadata_obj = MetaData()


user_request_booking_hostel_view = Table('user_request_booking_hostel_view', metadata_obj,
          Column('full_name', VARCHAR(255)),
          Column('user_id', Integer),
          Column('faculty_name', VARCHAR(255)),
          Column('university_id', Integer),
          Column('short_university_name', VARCHAR(50)),
          Column('rector_first_name', VARCHAR(255)),
          Column('rector_last_name', VARCHAR(255)),
          Column('rector_middle_name', VARCHAR(255)),
          Column('speciality_code', Integer),
          Column('speciality_name', VARCHAR(255)),
          Column('course', Integer),
          Column('educ_level', VARCHAR(1)),
          Column('date_today', DATETIME),
          Column('start_year', Integer),
          Column('finish_year', Integer),
          Column('gender', VARCHAR(1)))
