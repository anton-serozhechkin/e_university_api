from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, ForeignKey, DateTime)


metadata_obj = MetaData()

user_request = Table('user_request', metadata_obj,
          Column('user_request_id', Integer, primary_key=True),
          Column('user_id', Integer, ForeignKey("user.user_id")),
          Column('service_id', Integer, ForeignKey("service.service_id")),
          Column('date_created', DateTime),
          Column('comment', VARCHAR(255)),
          Column('faculty_id', Integer, ForeignKey("faculty.faculty_id")),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('status_id', Integer, ForeignKey("status.status_id")))
