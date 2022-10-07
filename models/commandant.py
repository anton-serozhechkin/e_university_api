from sqlalchemy import (Column, VARCHAR, INTEGER)
from sqlalchemy.orm import relationship

from db import Base


class Commandant(Base):
    __tablename__ = 'commandant'

    commandant_id = Column(INTEGER, primary_key=True)
    full_name = Column(VARCHAR(length=255))
    telephone_number = Column(VARCHAR(length=50))

    hostel = relationship("Hostel", back_populates="commandant")

    def __repr__(self):
        return (f'{self.__class__.__name__}(commandant_id="{self.commandant_id}",full_name="{self.full_name}",'
                f'telephone_number="{self.telephone_number}")')
