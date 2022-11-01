from apps.common.db import Base

from sqlalchemy import (MetaData, Column, INTEGER, VARCHAR, ForeignKey, Table, DECIMAL)
from sqlalchemy.orm import relationship

metadata_obj = MetaData()


class Hostel(Base):
    __tablename__ = 'hostel'

    hostel_id = Column(INTEGER, primary_key=True, nullable=False)
    number = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(length=100), nullable=False)
    city = Column(VARCHAR(length=100), nullable=False)
    street = Column(VARCHAR(length=100), nullable=False)
    build = Column(VARCHAR(length=10), nullable=False)
    month_price = Column(DECIMAL(4, 2))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    commandant_id = Column(INTEGER, ForeignKey("commandant.commandant_id"), nullable=False)

    university = relationship('University', back_populates='hostels')
    commandant = relationship('Commandant', back_populates='hostel', lazy="joined")
    user_request_reviews = relationship('UserRequestReview', back_populates='hostel')

    def __repr__(self):
        return f'{self.__class__.__name__}(hostel_id="{self.hostel_id}",' \
               f'number="{self.number}",name="{self.name}",city="{self.city}",street="{self.street}",' \
               f'build="{self.build}",month_price="{self.month_price}",university_id="{self.university_id}",commandant_id="{self.commandant_id}")'


class Commandant(Base):
    __tablename__ = 'commandant'

    commandant_id = Column(INTEGER, primary_key=True, nullable=False)
    full_name = Column(VARCHAR(length=255), nullable=False)
    telephone_number = Column(VARCHAR(length=50), nullable=False, unique=True)

    hostel = relationship("Hostel", back_populates="commandant")

    def __repr__(self):
        return (f'{self.__class__.__name__}(commandant_id="{self.commandant_id}",full_name="{self.full_name}",'
                f'telephone_number="{self.telephone_number}")')


class BedPlace(Base):
    __tablename__ = 'bed_place'

    bed_place_id = Column(INTEGER, primary_key=True, nullable=False)
    bed_place_name = Column(VARCHAR(length=50), nullable=False)

    user_request_review = relationship("UserRequestReview", back_populates='bed_place')

    def __repr__(self):
        return f'{self.__class__.__name__}(bed_place_id="{self.bed_place_id}", bed_place_name="{self.bed_place_name}")'


hostel_list_view = Table('hostel_list_view', metadata_obj,
                         Column('university_id', INTEGER),
                         Column('hostel_id', INTEGER),
                         Column('number', INTEGER),
                         Column('name', VARCHAR(100)),
                         Column('city', VARCHAR(100)),
                         Column('street', VARCHAR(100)),
                         Column('build', VARCHAR(10)),
                         Column('commandant_id', INTEGER),
                         Column('commandant_full_name', VARCHAR(255)))
