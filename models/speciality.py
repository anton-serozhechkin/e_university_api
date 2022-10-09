from models import faculty, student

from sqlalchemy import (Column,INTEGER, ForeignKey, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Speciality(Base):
    __tablename__ = 'speciality'

    speciality_id = Column(INTEGER, primary_key=True)
    code = Column(INTEGER)
    name = Column(VARCHAR(length=255))
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"))

    faculties = relationship("Faculty", back_populates="speciality")
    student = relationship("Student", back_populates="specialties")

    def __repr__(self):
        return f'{self.__class__.__name__}(speciality_id="{self.speciality_id}",code="{self.code}",name="{self.name}",' \
               f'faculty="{self.faculty}")'

