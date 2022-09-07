from sqlalchemy import (MetaData, Column, Table, Integer, JSON)


metadata_obj = MetaData()


speciality_list_view = Table('speciality_list_view', metadata_obj,
          Column('university_id', Integer),
          Column('speciality_id', Integer),
          Column('speciality_info', JSON))
