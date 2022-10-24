from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR)


metadata_obj = MetaData()


faculty_list_view = Table('faculty_list_view', metadata_obj,
          Column('faculty_id', Integer),
          Column('name', VARCHAR(255)),
          Column('shortname', VARCHAR(20)),
          Column('main_email', VARCHAR(50)),
          Column('university_id', Integer),
          Column('dekan_id', Integer),
          Column('decan_first_name', VARCHAR(255)),
          Column('decan_last_name', VARCHAR(255)),
          Column('decan_middle_name', VARCHAR(255)))
