# from sqlalchemy import (Column, INTEGER, DATETIME, JSON, VARCHAR)
#
# from db import Base
#
#
# class UserRequestDetailsView(Base):
#         __tablename__ = "user_request_details_view"
#
#         user_request_id = Column(INTEGER)
#         university_id = Column(INTEGER)
#         date_created = Column(DATETIME)
#         service_name = Column(VARCHAR(length=255))
#         status_name = Column(VARCHAR(length=50))
#         status_id = Column(INTEGER)
#         comment = Column(VARCHAR(length=255))
#         hostel_name = Column(JSON)
#         room_number = Column(INTEGER)
#         bed_place_name = Column(VARCHAR(length=50))
#         date_review = Column(INTEGER)
#         remark = Column(VARCHAR(length=255))
#         documents = Column(JSON)
#
#         def __repr__(self):
#                 return f'{self.__class__.__name__}(user_request_id="{self.user_request_id}", university_id="{self.university_id}",' \
#                        f'date_created="{self.date_created}", service_name="{self.service_name}", status_name="{self.status_name}",' \
#                        f'status_id="{self.status_id}", comment="{self.comment}", hostel_name="{self.hostel_name}", ' \
#                        f'room_number="{self.room_number}", bed_place_name="{self.bed_place_name}", date_review="{self.date_review}", remark="{self.remark}", documents="{self.documents}")'
#
from sqlalchemy import (MetaData, Column, Table, Integer, DateTime, JSON, VARCHAR)


metadata_obj = MetaData()


user_request_details_view = Table('user_request_details_view', metadata_obj,
        Column('user_request_id', Integer),
        Column('university_id', Integer),
        Column('date_created', DateTime),
        Column('service_name', VARCHAR(255)),
        Column('status_name', VARCHAR(50)),
        Column('status_id', Integer),
        Column('comment', VARCHAR(255)),
        Column('hostel_name', JSON),
        Column('room_number', Integer),
        Column('bed_place_name', VARCHAR(50)),
        Column('date_review', DateTime),
        Column('remark', VARCHAR(255)),
        Column('documents', JSON))