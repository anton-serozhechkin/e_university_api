# from sqlalchemy import (Column, INTEGER, VARCHAR, DATETIME, JSON, PrimaryKeyConstraint)
#
# from db import Base
#
#
# class UserRequestListView(Base):
#     __tablename__ = "user_request_list_view"
#
#     university_id = Column(INTEGER)
#     user_id = Column(INTEGER)
#     user_request_id = Column(INTEGER)
#     service_name = Column(VARCHAR(length=255))
#     status = Column(JSON)
#     date_created = Column(DATETIME)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(university_id="{self.university_id}", user_id="{self.user_id}", user_request_id="{self.user_request_id}",' \
#                f'service_name="{self.service_name}", status="{self.status}", date_created="{self.date_created}")'

from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, DateTime, JSON)


metadata_obj = MetaData()


user_request_list_view = Table('user_request_list_view', metadata_obj,
          Column('university_id', Integer),
          Column('user_id', Integer),
          Column('user_request_id', Integer),
          Column('service_name', VARCHAR(255)),
          Column('status', JSON),
          Column('date_created', DateTime))