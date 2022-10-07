from sqlalchemy import (Column, INTEGER, VARCHAR)

from db import Base


STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}


class Status(Base):
    __tablename__ = "status"

    status_id = Column(INTEGER, primary_key=True)
    status_name = Column(VARCHAR(length=50))

    def __repr__(self):
        return f'{self.__class__.__name__}(status_id="{self.status_id}",status_name="{self.status_name}")'

