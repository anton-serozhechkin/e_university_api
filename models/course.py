from models import student

from sqlalchemy import (Column, INTEGER)
from sqlalchemy.orm import relationship

from db import Base


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(INTEGER, primary_key=True, nullable=False)
    value = Column(INTEGER, nullable=False)

    student = relationship('Student', back_populates='courses')
    def __repr__(self):
        return f'{self.__class__.__name__}(course_id="{self.course_id}", value="{self.value}")'
