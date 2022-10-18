from models import dekan, university, speciality, student, user_faculty

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base


class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    shortname = Column(VARCHAR(length=20))
    main_email = Column(VARCHAR(length=50))
    dekan_id = Column(INTEGER, ForeignKey('dekan.dekan_id'))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)

    dekan = relationship("Dekan", back_populates="faculties")
    university = relationship("University", back_populates="faculties")
    speciality = relationship("Speciality", back_populates="faculties")
    student = relationship("Student", back_populates="faculties")
    faculty = relationship("UserFaculty", back_populates="faculties")
    user_request = relationship("UserRequest", back_populates="faculties")

    def __repr__(self):
        return f'{self.__class__.__name__}(faculty_id="{self.faculty_id}", name="{self.name}", shortname="{self.shortname}", ' \
               f'main_email="{self.main_email}", dekan_id="{self.dekan_id}", university_id="{self.university_id}")'
