from models import student

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, TIMESTAMP)
from sqlalchemy.orm import relationship

from db import Base


class OneTimeToken(Base):
    __tablename__ = 'one_time_token'

    token_id = Column(INTEGER, primary_key=True, nullable=False)
    token = Column(VARCHAR(length=255), nullable=False)
    expires = Column(TIMESTAMP, nullable=False)
    student_id = Column(INTEGER, ForeignKey("student.student_id"), nullable=False)

    student = relationship("Student", back_populates="one_time_token")

    def __repr__(self):
        return f'{self.__class__.__name__}(token_id="{self.token_id}",token="{self.token}",expires="{self.expires}",student_id="{self.student_id}")'

