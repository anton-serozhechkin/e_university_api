from sqlalchemy import (
    BOOLEAN,
    DATETIME,
    INTEGER,
    JSON,
    VARCHAR,
    Column,
    ForeignKey,
    MetaData,
    Table,
    func,
)
from sqlalchemy.orm import relationship

from apps.common.db import Base
from apps.common.utils import AwareDateTime

metadata_obj = MetaData()


class User(Base):
    __tablename__ = "user"

    user_id = Column(INTEGER, primary_key=True, nullable=False)
    login = Column(VARCHAR(length=50), nullable=False, unique=True)
    password = Column(VARCHAR(length=50), nullable=False)
    last_visit_at = Column(AwareDateTime, default=func.now(), nullable=False)
    email = Column(VARCHAR(length=100), nullable=False, unique=True)
    is_active = Column(BOOLEAN, default=False)
    role_id = Column(
        INTEGER,
        ForeignKey("role.role_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    created_at = Column(AwareDateTime, default=func.now(), nullable=False)
    updated_at = Column(AwareDateTime, default=func.now(), nullable=False)

    student = relationship("Student", back_populates="user")
    user_request_reviews = relationship(
        "UserRequestReview", back_populates="reviewer_user"
    )
    faculties = relationship(
        "Faculty", secondary="user_faculty", back_populates="users"
    )
    user_requests = relationship("UserRequest", back_populates="user")
    roles = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(user_id="{self.user_id}", login="{self.login}",'
            f' password="{self.password}", last_visit_at="{self.last_visit_at}",'
            f' email="{self.email}", is_active="{self.is_active}",'
            f' role_id="{self.role_id}")'
        )


class OneTimeToken(Base):
    __tablename__ = "one_time_token"

    token_id = Column(INTEGER, primary_key=True, nullable=False)
    token = Column(VARCHAR(length=255), nullable=False)
    expires_at = Column(AwareDateTime, nullable=False)
    student_id = Column(
        INTEGER,
        ForeignKey("student.student_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    student = relationship("Student", back_populates="one_time_tokens")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(token_id="{self.token_id}",'
            f' token="{self.token}", expires_at="{self.expires_at}",'
            f' student_id="{self.student_id}")'
        )


class Student(Base):
    __tablename__ = "student"

    student_id = Column(INTEGER, primary_key=True, nullable=False)
    last_name = Column(VARCHAR(length=50), nullable=False)
    first_name = Column(VARCHAR(length=50), nullable=False)
    middle_name = Column(VARCHAR(length=50))
    telephone_number = Column(VARCHAR(length=50), nullable=False, unique=True)
    gender = Column(VARCHAR(length=1), nullable=False)
    course_id = Column(
        INTEGER,
        ForeignKey("course.course_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    speciality_id = Column(
        INTEGER,
        ForeignKey("speciality.speciality_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        INTEGER,
        ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    faculty_id = Column(
        INTEGER,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    created_at = Column(AwareDateTime, default=func.now(), nullable=False)
    updated_at = Column(AwareDateTime, default=func.now(), nullable=False)

    course = relationship("Course", sync_backref=False, lazy="joined")
    speciality = relationship("Speciality", sync_backref=False)
    user = relationship("User", back_populates="student")
    faculty = relationship("Faculty", back_populates="students")
    one_time_tokens = relationship("OneTimeToken", back_populates="student")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(student_id="{self.student_id}",'
            f' first_name="{self.first_name}", middle_name="{self.middle_name}",'
            f' last_name="{self.last_name}",'
            f' telephone_number="{self.telephone_number}", gender="{self.gender}",'
            f' course_id="{self.course_id}", speciality_id="{self.speciality_id}",'
            f' user_id="{self.user_id}", faculty_id="{self.faculty_id}")'
        )


class UserFaculty(Base):
    __tablename__ = "user_faculty"

    user_id = Column(
        INTEGER,
        ForeignKey("user.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    faculty_id = Column(
        INTEGER,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(user_id="{self.user_id}",'
            f' faculty_id="{self.faculty_id}")'
        )


students_list_view = Table(
    "students_list_view",
    metadata_obj,
    Column("student_id", INTEGER),
    Column("student_full_name", JSON),
    Column("telephone_number", VARCHAR(50)),
    Column("user_id", INTEGER),
    Column("university_id", INTEGER),
    Column("faculty_id", INTEGER),
    Column("speciality_id", INTEGER),
    Column("course_id", INTEGER),
    Column("gender", VARCHAR(1)),
)


user_list_view = Table(
    "user_list_view",
    metadata_obj,
    Column("user_id", INTEGER),
    Column("login", VARCHAR(50)),
    Column("last_visit_at", DATETIME),
    Column("email", VARCHAR(50)),
    Column("role", JSON),
    Column("is_active", BOOLEAN),
    Column("university_id", INTEGER),
    Column("faculties", JSON),
)
