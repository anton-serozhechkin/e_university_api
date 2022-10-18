from models import university, commandant, user_request_review

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, FLOAT)
from sqlalchemy.orm import relationship

from db import Base


class Hostel(Base):
    __tablename__ = 'hostel'

    hostel_id = Column(INTEGER, primary_key=True, nullable=False)
    number = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(length=100), nullable=False)
    city = Column(VARCHAR(length=100), nullable=False)
    street = Column(VARCHAR(length=100), nullable=False)
    build = Column(VARCHAR(length=10), nullable=False)
    month_price = Column(FLOAT)
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    commandant_id = Column(INTEGER, ForeignKey("commandant.commandant_id"), nullable=False)

    university = relationship('University', back_populates='hostels')
    commandant = relationship('Commandant', back_populates='hostel')
    user_request_reviews = relationship('UserRequestReview', back_populates='hostels')


    def __repr__(self):
        return f'{self.__class__.__name__}(hostel_id="{self.hostel_id}",' \
               f'number="{self.number}",name="{self.name}",city="{self.city}",street="{self.street}",' \
               f'build="{self.build}",month_price="{self.month_price}",university_id="{self.university_id}",commandant_id="{self.commandant_id}")'
