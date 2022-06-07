from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, 
                        BOOLEAN, TIMESTAMP)

from e_university_api.models.role import role


metadata_obj = MetaData()

user = Table('user', metadata_obj,
          Column('user_id', Integer, primary_key=True),
          Column('login', VARCHAR(50)),
          Column('password', VARCHAR(50)),
          Column('last_visit', TIMESTAMP),
          Column('email', VARCHAR(100)), 
          Column('is_active', BOOLEAN),
          Column('role_id', Integer, ForeignKey("role.role_id"), nullable=True))
