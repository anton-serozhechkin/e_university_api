from models import university

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Rector(Base):
    __tablename__ = 'rector'

    rector_id = Column(INTEGER, primary_key=True, nullable=False)
    full_name = Column(VARCHAR(length=255), nullable=False)

    university = relationship("University", back_populates="rector")
    def __str__(self):
        return f'{self.__class__.__name__}(rector_id="{self.rector_id}",full_name="{self.full_name}")'


