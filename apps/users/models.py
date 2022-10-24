from apps.common.db import Base

from sqlalchemy import (MetaData, Column, Table, INTEGER, VARCHAR, ForeignKey, BOOLEAN, TIMESTAMP, JSON)
from sqlalchemy.orm import relationship

metadata_obj = MetaData()


class User(Base):
    __tablename__ = "user"

    user_id = Column(INTEGER, primary_key=True, nullable=False)
    login = Column(VARCHAR(length=50), nullable=False, unique=True)
    password = Column(VARCHAR(length=50), nullable=False)
    last_visit = Column(TIMESTAMP)
    email = Column(VARCHAR(length=100), nullable=False, unique=True)
    is_active = Column(BOOLEAN, default=False)
    role_id = Column(INTEGER, ForeignKey("role.role_id"), nullable=True)

    student = relationship("Student", back_populates="user")
    user_request_reviews = relationship("UserRequestReview", back_populates="reviewer_user")
    faculties = relationship("Faculty", secondary="user_faculty", back_populates="users")
    user_requests = relationship("UserRequest", back_populates="user")
    roles = relationship("Role", back_populates="users")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id="{self.user_id}", login="{self.login}", password="{self.password}", ' \
               f'last_visit="{self.last_visit}", email="{self.email}", is_active="{self.is_active}", role_id="{self.role_id}")'


class OneTimeToken(Base):
    __tablename__ = 'one_time_token'

    token_id = Column(INTEGER, primary_key=True, nullable=False)
    token = Column(VARCHAR(length=255), nullable=False)
    expires = Column(TIMESTAMP, nullable=False)
    student_id = Column(INTEGER, ForeignKey("student.student_id"), nullable=False)

    student = relationship("Student", back_populates="one_time_tokens")

    def __repr__(self):
        return f'{self.__class__.__name__}(token_id="{self.token_id}",token="{self.token}",expires="{self.expires}",student_id="{self.student_id}")'


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(INTEGER, primary_key=True, nullable=False)
    full_name = Column(VARCHAR(length=255), nullable=False)
    telephone_number = Column(INTEGER, nullable=False, unique=True)
    gender = Column(VARCHAR(length=1), nullable=False)
    course_id = Column(INTEGER, ForeignKey("course.course_id"), nullable=False)
    speciality_id = Column(INTEGER, ForeignKey("speciality.speciality_id"), nullable=False)
    user_id = Column(INTEGER, ForeignKey("user.user_id"))
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"), nullable=False)

    course = relationship("Course", sync_backref=False, lazy="joined")
    speciality = relationship("Speciality", sync_backref=False)
    user = relationship("User", back_populates="student")
    faculty = relationship("Faculty", back_populates="students")
    one_time_tokens = relationship("OneTimeToken", back_populates="student")

    def __repr__(self):
        return f'{self.__class__.__name__}(student_id="{self.student_id}",full_name="{self.full_name}",' \
               f'telephone_number="{self.telephone_number}",gender="{self.gender}",' \
               f'course_id="{self.course_id}",speciality_id="{self.speciality_id}",user_id="{self.user_id}",faculty_id="{self.faculty_id}")'


class UserFaculty(Base):
    __tablename__ = "user_faculty"

    user_id = Column(INTEGER, ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, primary_key=True)
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, primary_key=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id="{self.user_id}", faculty_id="{self.faculty_id}")'


students_list_view = Table('students_list_view', metadata_obj,
                           Column('student_id', INTEGER),
                           Column('student_full_name', VARCHAR(255)),
                           Column('telephone_number', INTEGER),
                           Column('user_id', INTEGER),
                           Column('university_id', INTEGER),
                           Column('faculty_id', INTEGER),
                           Column('speciality_id', INTEGER),
                           Column('course_id', INTEGER),
                           Column('gender', VARCHAR(1)))

user_list_view = Table('user_list_view', metadata_obj,
                       Column('user_id', INTEGER),
                       Column('login', VARCHAR(50)),
                       Column('last_visit', TIMESTAMP),
                       Column('email', VARCHAR(50)),
                       Column('role', JSON),
                       Column('is_active', BOOLEAN),
                       Column('university_id', INTEGER),
                       Column('faculties', JSON))
