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
