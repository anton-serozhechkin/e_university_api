from sqlalchemy import (MetaData, Column, Table, Integer, DateTime, JSON, VARCHAR)


metadata_obj = MetaData()


user_request_details_view = Table('user_request_details_view', metadata_obj,
        Column('user_request_id', Integer),
        Column('university_id', Integer),
        Column('date_created', DateTime),
        Column('service_name', VARCHAR(255)),
        Column('user_request_status_name', VARCHAR(50)),
        Column('user_request_status_id', Integer),
        Column('comment', VARCHAR(255)),
        Column('hostel_name', JSON),
        Column('room_number', Integer),
        Column('bed_place_name', VARCHAR(50)),
        Column('date_review', DateTime),
        Column('remark', VARCHAR(255)),
        Column('documents', JSON))
