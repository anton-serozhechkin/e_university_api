from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)


metadata_obj = MetaData()


university = Table('university', metadata_obj,
             Column('university_id', Integer, primary_key = True),
             Column('university_name', VARCHAR(255)),
             Column('logo', VARCHAR(255)),
             Column('rector_id', Integer), ForeignKey("rector.rector_id"))
