from models import course, speciality, user, faculty, one_time_token

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base

class Student(Base):
    __tablename__ = 'student'

    student_id = Column(INTEGER, primary_key=True)
    full_name = Column(VARCHAR(length=255))
    telephone_number = Column(INTEGER)
    gender = Column(VARCHAR(length=1))
    course_id = Column(INTEGER, ForeignKey("course.course_id"))
    speciality_id = Column(INTEGER, ForeignKey("speciality.speciality_id"))
    user_id = Column(INTEGER, ForeignKey("user.user_id"))
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"))

    courses = relationship("Course", back_populates="student")
    specialties = relationship("Speciality", back_populates="student")
    users = relationship("User", back_populates="student")
    faculties = relationship("Faculty", back_populates="student")
    one_time_token = relationship("OneTimeToken", back_populates="student")

    def __repr__(self):
        return f'{self.__class__.__name__}(student_id="{self.student_id}",full_name="{self.full_name}",' \
               f'telephone_number="{self.telephone_number}",gender="{self.gender}",faculty="{self.faculty}",' \
               f'course="{self.course}",speciality="{self.speciality}",user="{self.user}")'