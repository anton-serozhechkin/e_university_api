from models import requisites, user_request

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Service(Base):
    __tablename__ = 'service'

    service_id = Column(INTEGER, primary_key=True)
    service_name = Column(VARCHAR(length=255))

    requisites = relationship("Requisites", back_populates="service")
    user_request = relationship("UserRequest", back_populates="service")

    def __repr__(self):
        return f'{self.__class__.__name__}(service_id="{self.service_id}",service_name="{self.service_name}")'

