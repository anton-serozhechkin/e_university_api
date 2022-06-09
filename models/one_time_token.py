from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, TIMESTAMP)


from models.student import student


metadata_obj = MetaData()

one_time_token = Table('one_time_token', metadata_obj,
          Column('student_id', Integer, ForeignKey("student.student_id"), nullable=False),
          Column('token_id', Integer, primary_key=True),
          Column('token', VARCHAR(255), nullable=False),
          Column('expires', TIMESTAMP, nullable=False))
