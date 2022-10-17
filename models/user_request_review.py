from sqlalchemy import (MetaData, Column, Table, Integer, DateTime, ForeignKey, VARCHAR, FLOAT)


metadata_obj = MetaData()


user_request_review = Table('user_request_review', metadata_obj,
          Column('user_request_review_id', Integer, primary_key=True),
          Column('university_id', Integer, ForeignKey("university.university_id")),
          Column('user_request_id', Integer, ForeignKey("user_request.user_request_id")),
          Column('date_created', DateTime),
          Column('reviewer', Integer, ForeignKey("user.user_id")),
          Column('hostel_id', Integer, ForeignKey("hostel.hostel_id")),
          Column('room_number', Integer),
          Column('start_date_accommodation', DateTime),
          Column('end_date_accommodation', DateTime),
          Column('total_sum', FLOAT),
          Column('payment_deadline', DateTime),
          Column('remark', VARCHAR(255)),
          Column('date_review', DateTime),
          Column('bed_place_id', Integer, ForeignKey("bed_place.bed_place_id")))


