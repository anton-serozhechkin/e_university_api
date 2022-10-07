from models import university, commandant, user_request_review

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, FLOAT)
from sqlalchemy.orm import relationship

from db import Base


class Hostel(Base):
    __tablename__ = 'hostel'

    hostel_id = Column(INTEGER, primary_key=True)
    number = Column(INTEGER)
    name = Column(VARCHAR(length=100))
    city = Column(VARCHAR(length=100))
    street = Column(VARCHAR(length=100))
    build = Column(VARCHAR(length=10))
    month_price = Column(FLOAT)
    university_id = Column(INTEGER, ForeignKey("university.university.id"))
    commandant_id = Column(INTEGER, ForeignKey("commandant.commandant.id"))

    university = relationship('University', back_populates='hostels')
    commandant = relationship('Commandant', back_populates='hostel')
    user_request_reviews = relationship('UserRequestReview', back_populates='hostels')


    def __repr__(self):
        return f'{self.__class__.__name__}(hostel_id="{self.hostel_id}",university="{self.university}",' \
               f'number="{self.number}",name="{self.name}",city="{self.city}",street="{self.street}",' \
               f'build="{self.build}",month_price="{self.month_price}",commandant="{self.commandant}")'

