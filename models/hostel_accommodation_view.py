# from sqlalchemy import (Column, INTEGER, JSON, TIMESTAMP, FLOAT, VARCHAR)
#
# from db import Base
#
#
# class HostelAccommodationView(Base):
#     __tablename__ = 'hostel_accommodation_view'
#
#     university_id = Column(INTEGER)
#     user_request_review_id = Column(INTEGER)
#     user_request_id = Column(INTEGER)
#     hostel_name = Column(JSON)
#     hostel_address = Column(JSON)
#     room_number = Column(INTEGER)
#     bed_place_name = Column(VARCHAR(length=50))
#     month_price = Column(FLOAT)
#     start_date_accommodation = Column(TIMESTAMP)
#     end_date_accommodation = Column(TIMESTAMP)
#     total_sum = Column(FLOAT)
#     iban = Column(VARCHAR(length=100))
#     university_name = Column(VARCHAR(length=255))
#     organisation_code = Column(VARCHAR(length=50))
#     payment_recognition = Column(VARCHAR(length=255))
#     commandant_full_name = Column(VARCHAR(length=255))
#     telephone_number = Column(VARCHAR(length=50))
#     documents = Column(JSON)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(university_id={self.university_id}", user_request_review_id="{self.user_request_review_id}",' \
#                f'user_request_id="{self.user_request_id}",hostel_name="{self.hostel_name}",hostel_address="{self.hostel_address}",' \
#                f'room_number="{self.room_number}",bed_place_name="{self.bed_place_name}",month_price="{self.month_price}",' \
#                f'start_date_accommodation="{self.start_date_accommodation}",end_date_accommodation="{self.end_date_accommodation}",' \
#                f'total_sum="{self.total_sum}",iban="{self.iban}",university_name="{self.university_name}", ' \
#                f'organisation_code="{self.organisation_code}", payment_recognition="{self.payment_recognition}",' \
#                f'commandant_full_name="{self.commandant_full_name}",telephone_number="{self.telephone_number}",' \
#                f'documents="{self.documents}")'
#
from sqlalchemy import (MetaData, Column, Table, Integer, JSON, TIMESTAMP, Float, VARCHAR)


metadata_obj = MetaData()

hostel_accommodation_view = Table('hostel_accommodation_view', metadata_obj,
          Column('university_id', Integer),
          Column('user_request_review_id', Integer),
          Column('user_request_id', Integer),
          Column('hostel_name', JSON),
          Column('hostel_address', JSON),
          Column('room_number', Integer),
          Column('bed_place_name', VARCHAR(50)),
          Column('month_price', Float),
          Column('start_date_accommodation', TIMESTAMP),
          Column('end_date_accommodation', TIMESTAMP),
          Column('total_sum', Float),
          Column('iban', VARCHAR(100)),
          Column('university_name', VARCHAR(255)),
          Column('organisation_code', VARCHAR(50)),
          Column('payment_recognation', VARCHAR(255)),
          Column('commandant_full_name', VARCHAR(255)),
          Column('telephone_number', VARCHAR(50)),
          Column('documents', JSON))