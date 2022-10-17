from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}


class Status(Base):
    __tablename__ = "user_request_status"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(length=50))

    user_request = relationship("UserRequest", back_populates="user_request_status")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_status_id="{self.id}",user_request_status_name="{self.name}")'

