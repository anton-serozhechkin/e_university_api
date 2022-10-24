from models import course, speciality, user, faculty, one_time_token

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(INTEGER, primary_key=True, nullable=False)
    first_name = Column(VARCHAR(length=255), nullable=False)
    last_name = Column(VARCHAR(length=255), nullable=False)
    middle_name = Column(VARCHAR(length=255), nullable=True)
    telephone_number = Column(INTEGER, nullable=False, unique=True)
    gender = Column(VARCHAR(length=1), nullable=False)
    course_id = Column(INTEGER, ForeignKey("course.course_id"), nullable=False)
    speciality_id = Column(INTEGER, ForeignKey("speciality.speciality_id"), nullable=False)
    user_id = Column(INTEGER, ForeignKey("user.user_id"))
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"), nullable=False)

    courses = relationship("Course", back_populates="student")
    specialties = relationship("Speciality", back_populates="student")
    users = relationship("User", back_populates="student")
    faculties = relationship("Faculty", back_populates="student")
    one_time_token = relationship("OneTimeToken", back_populates="student")

    def __repr__(self):
        return f'{self.__class__.__name__}(student_id="{self.student_id}",first_name="{self.first_name}",' \
               f'last_name="{self.last_name}",' \ 
               f'telephone_number="{self.telephone_number}",gender="{self.gender}",' \
               f'course_id="{self.course_id}",speciality_id="{self.speciality_id}",user_id="{self.user_id}",' \
               f'faculty_id="{self.faculty_id}")'
