from models import university, service

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base


class Requisites(Base):
    __tablename__ = 'requisites'

    iban = Column(VARCHAR(length=100))
    organisation_code = Column(VARCHAR(length=50))
    payment_recognition = Column(VARCHAR(length=255))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), primary_key=True)
    service_id = Column(INTEGER, ForeignKey("service.service_id"))

    university = relationship("University", back_populates="requisites")
    service = relationship("Service", back_populates="requisites")

    def __repr__(self):
        return f'{self.__class__.__name__}(iban="{self.iban}",organisation_code="{self.organisation_code}",' \
               f'payment_recognition="{self.payment_recognation}",university_id="{self.university_id}",service_id="{self.service_id}")'
