from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, JSON)


metadata_obj = MetaData()


university = Table('university', metadata_obj,
             Column('university_id', Integer, primary_key = True),
             Column('university_name', VARCHAR(255)),
             Column('logo', VARCHAR(255)),
             Column('rector_id', Integer, ForeignKey("rector.rector_id")))


faculty = Table('faculty', metadata_obj,
          Column('faculty_id', Integer, primary_key = True),
          Column('name', VARCHAR(255), nullable=False),
          Column('shortname', VARCHAR(20)),
          Column('main_email', VARCHAR(50)),
          Column('dekan_id', Integer, ForeignKey("dekan.dekan_id")),
          Column('university_id', Integer, ForeignKey("university.university_id"), nullable=False))


speciality = Table('speciality', metadata_obj,
          Column('speciality_id', Integer, primary_key=True),
          Column('code', Integer),
          Column('name', VARCHAR(255)),
          Column('university_id', Integer, ForeignKey("university.university_id"), nullable=False))


dean = Table('dean', metadata_obj,
          Column('dean_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)))


rector = Table('rector', metadata_obj,
          Column('rector_id', Integer, primary_key=True),
          Column('full_name', VARCHAR(255)))


course = Table('course', metadata_obj,
          Column('course_id', Integer, primary_key=True),
          Column('value', Integer))


faculty_list_view = Table('faculty_list_view', metadata_obj,
          Column('faculty_id', Integer),
          Column('name', VARCHAR(255)),
          Column('shortname', VARCHAR(20)),
          Column('main_email', VARCHAR(50)),
          Column('university_id', Integer),
          Column('dekan_id', Integer),
          Column('decan_full_name', VARCHAR(255)))


speciality_list_view = Table('speciality_list_view', metadata_obj,
          Column('faculty_id', Integer),
          Column('speciality_id', Integer),
          Column('university_id', Integer),
          Column('speciality_info', JSON))
