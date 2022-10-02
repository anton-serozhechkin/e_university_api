from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey)

metadata_obj = MetaData()

role = Table('role', metadata_obj,
          Column('role_id', Integer, primary_key=True),
          Column('role_name', VARCHAR(50)))

action = Table('action', metadata_obj,
          Column('action_id', Integer, primary_key=True),
          Column('action_name', VARCHAR(50)),
          Column('role_id', Integer, ForeignKey("role.role_id", nullable=False)))
