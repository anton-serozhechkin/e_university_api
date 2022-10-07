# from sqlalchemy import (Column, INTEGER, VARCHAR, TIMESTAMP, JSON, BOOLEAN, PrimaryKeyConstraint)
#
# from db import Base
#
#
# class UserListView(Base):
#     __tablename__ = "user_list_view"
#
#     user_id = Column(INTEGER)
#     login = Column(VARCHAR(length=50))
#     last_visit = Column(TIMESTAMP)
#     email = Column(VARCHAR(length=50))
#     role = Column(JSON)
#     is_active = Column(BOOLEAN)
#     university_id = Column(INTEGER)
#     faculties = Column(JSON)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(user_id="{self.user_id}", login="{self.login}", last_visit="{self.last_visit}", ' \
#                f'email="{self.email}", role="{self.role}", is_active="{self.is_active}", university_id="{self.university_id}", ' \
#                f'faculties="{self.faculties}")'
from sqlalchemy import (MetaData, Column, Table, Integer, VARCHAR, TIMESTAMP, JSON, BOOLEAN)


metadata_obj = MetaData()


user_list_view = Table('user_list_view', metadata_obj,
          Column('user_id', Integer),
          Column('login', VARCHAR(50)),
          Column('last_visit', TIMESTAMP),
          Column('email', VARCHAR(50)),
          Column('role', JSON),
          Column('is_active', BOOLEAN),
          Column('university_id', Integer),
          Column('faculties', JSON))