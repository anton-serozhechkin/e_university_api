from sqlalchemy import (MetaData, Column, Table, Integer, JSON, VARCHAR)


metadata_obj = MetaData()


accommodation_order_view = Table('accommodation_order_view', metadata_obj,
        Column('university_name', VARCHAR(255)),
        Column('short_university_name', VARCHAR(255)),
        Column('full_name', VARCHAR(255)),
        Column('faculty_shortname', VARCHAR(20)),
        Column('city', VARCHAR(100)),
        Column('room_number', Integer),
        Column('hostel_number', Integer),
        Column('hostel_address', JSON),
        Column('dekan_full_name', VARCHAR(255)))
