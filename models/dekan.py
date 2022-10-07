from models import faculty

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Dekan(Base):
    __tablename__ = 'dekan'

    dekan_id = Column(INTEGER, primary_key=True)
    full_name = Column(VARCHAR(length=255))

    faculties = relationship("Faculty", back_populates="dekan")

    def __repr__(self):
        return f'{self.__class__.__name__}(dekan_id="{self.dekan_id}", full_name="{self.full_name}")'

