from models import hostel

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Commandant(Base):
    __tablename__ = 'commandant'

    commandant_id = Column(INTEGER, primary_key=True, nullable=False)
    first_name = Column(VARCHAR(length=255), nullable=False)
    last_name = Column(VARCHAR(length=255), nullable=False)
    middle_name = Column(VARCHAR(length=255), nullable=True)
    telephone_number = Column(VARCHAR(length=50), nullable=False, unique=True)

    hostel = relationship("Hostel", back_populates="commandant")

    def __repr__(self):
        return (f'{self.__class__.__name__}(commandant_id="{self.commandant_id}",first_name="{self.first_name}",'
                f'last_name="{self.last_name}")'
                f'middle_name="{self.middle_name}")'
                f'telephone_number="{self.telephone_number}")')
