from models import university

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Rector(Base):
    __tablename__ = 'rector'

    rector_id = Column(INTEGER, primary_key=True, nullable=False)
    first_name = Column(VARCHAR(length=255), nullable=False)
    last_name = Column(VARCHAR(length=255), nullable=False)
    middle_name = Column(VARCHAR(length=255), nullable=True)

    university = relationship("University", back_populates="rector")

    def __str__(self):
        return f'{self.__class__.__name__}(rector_id="{self.rector_id}",first_name="{self.first_name}", ' \
               f'last_name="{self.last_name}", middle_name="{self.middle_name}")'


