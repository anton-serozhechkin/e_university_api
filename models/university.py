from models import rector, faculty, hostel, requisites, user_request_review

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base

class University(Base):
    __tablename__ = "university"

    university_id = Column(INTEGER, primary_key=True)
    university_name = Column(VARCHAR(length=255))
    logo = Column(VARCHAR(length=255))
    rector_id = Column(INTEGER, ForeignKey("rector.rector_id"))

    rector = relationship("Rector", back_populates="university")
    faculties = relationship("Faculty", back_populates="university")
    hostels = relationship("Hostel", back_populates="university")
    requisites = relationship("Requisites", back_populates="university")
    user_request_reviews = relationship("UserRequestReview", back_populates="university")
    user_request = relationship("UserRequest", back_populates="university")

    def __repr__(self):
        return f'{self.__class__.__name__}(university_id="{self.university_id}", university_name="{self.university_name}",' \
               f'logo="{self.logo}", rector_id="{self.rector_id}")'
