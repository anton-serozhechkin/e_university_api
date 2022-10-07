# from sqlalchemy import (Column, INTEGER, JSON, PrimaryKeyConstraint)
#
# from db import Base
#
#
# class UserRequestExistView(Base):
#     __tablename__ = 'user_request_exist_view'
#
#     user_request_id = Column(INTEGER)
#     user_id = Column(INTEGER)
#     faculty_id = Column(INTEGER)
#     university_id = Column(INTEGER)
#     service_id = Column(INTEGER)
#     status = Column(JSON)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(user_request_id="{self.user_request_id}", user_id="{self.user_id}", ' \
#                f'faculty_id="{self.faculty_id}", university_id="{self.university_id}", service_id="{self.service_id}", status="{self.status}")'
from sqlalchemy import (MetaData, Column, Table, Integer, JSON)


metadata_obj = MetaData()


user_request_exist_view = Table('user_request_exist_view', metadata_obj,
          Column('user_request_id', Integer),
          Column('user_id', Integer),
          Column('faculty_id', Integer),
          Column('university_id', Integer),
          Column('service_id', Integer),
          Column('status', JSON))