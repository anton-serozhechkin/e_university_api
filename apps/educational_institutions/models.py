from sqlalchemy import INTEGER, JSON, VARCHAR, Column, ForeignKey, MetaData, Table
from sqlalchemy.orm import relationship

from apps.common.db import Base

metadata_obj = MetaData()


class University(Base):
    __tablename__ = "university"

    university_id = Column(INTEGER, primary_key=True, nullable=False)
    university_name = Column(VARCHAR(length=255), nullable=False)
    short_university_name = Column(VARCHAR(length=50), nullable=False)
    city = Column(VARCHAR(length=255), nullable=False)
    logo = Column(VARCHAR(length=255))
    rector_id = Column(
        INTEGER,
        ForeignKey("rector.rector_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    rector = relationship("Rector", back_populates="university")
    faculties = relationship("Faculty", back_populates="university")
    hostels = relationship("Hostel", back_populates="university")
    requisites = relationship("Requisites", back_populates="university")
    user_request_reviews = relationship(
        "UserRequestReview", back_populates="university"
    )
    user_requests = relationship("UserRequest", back_populates="university")
    service_document = relationship("ServiceDocument", back_populates="university")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(university_id="{self.university_id}", '
            f'university_name="{self.university_name}", city="{self.city}", '
            f'logo="{self.logo}", rector_id="{self.rector_id}")'
        )


class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    shortname = Column(VARCHAR(length=20))
    main_email = Column(VARCHAR(length=50))
    dean_id = Column(
        INTEGER,
        ForeignKey("dean.dean_id"),
        nullable=False,
    )
    university_id = Column(
        INTEGER,
        ForeignKey("university.university_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    dean = relationship("Dean", back_populates="faculty")
    university = relationship("University", back_populates="faculties")
    speciality = relationship("Speciality", back_populates="faculties")
    students = relationship("Student", back_populates="faculty")
    users = relationship("User", secondary="user_faculty", back_populates="faculties")
    user_requests = relationship("UserRequest", back_populates="faculty")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(faculty_id="{self.faculty_id}",'
            f' name="{self.name}", shortname="{self.shortname}",'
            f' main_email="{self.main_email}", dean_id="{self.dean_id}",'
            f' university_id="{self.university_id}"'
        )


class Speciality(Base):  # TODO: rename to "Specialty"
    __tablename__ = "speciality"  # TODO: rename to "specialty"

    speciality_id = Column(INTEGER, primary_key=True, nullable=False)
    code = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    faculty_id = Column(
        INTEGER,
        ForeignKey("faculty.faculty_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    faculties = relationship("Faculty", back_populates="speciality")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(speciality_id="{self.speciality_id}",'
            f' code="{self.code}", name="{self.name}", faculty_id="{self.faculty_id}")'
        )


class Dean(Base):
    __tablename__ = "dean"

    dean_id = Column(INTEGER, primary_key=True, nullable=False)
    last_name = Column(VARCHAR(length=50), nullable=False)
    first_name = Column(VARCHAR(length=50), nullable=False)
    middle_name = Column(VARCHAR(length=50))

    faculty = relationship("Faculty", back_populates="dean")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(dean_id="{self.dean_id}",'
            f' first_name="{self.first_name}", middle_name="{self.middle_name}",'
            f' last_name="{self.last_name}")'
        )


class Rector(Base):
    __tablename__ = "rector"

    rector_id = Column(INTEGER, primary_key=True, nullable=False)
    last_name = Column(VARCHAR(length=50), nullable=False)
    first_name = Column(VARCHAR(length=50), nullable=False)
    middle_name = Column(VARCHAR(length=50))

    university = relationship("University", back_populates="rector")

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}(rector_id="{self.rector_id}",'
            f' first_name="{self.first_name}", middle_name="{self.middle_name}",'
            f' last_name="{self.last_name}")'
        )


class Course(Base):
    __tablename__ = "course"

    course_id = Column(INTEGER, primary_key=True, nullable=False)
    value = Column(INTEGER, nullable=False)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(course_id="{self.course_id}",'
            f' value="{self.value}")'
        )


faculty_list_view = Table(
    "faculty_list_view",
    metadata_obj,
    Column("faculty_id", INTEGER),
    Column("name", VARCHAR(255)),
    Column("shortname", VARCHAR(20)),
    Column("main_email", VARCHAR(50)),
    Column("university_id", INTEGER),
    Column("dean_id", INTEGER),
    Column("dean_full_name", JSON),
)


speciality_list_view = Table(
    "speciality_list_view",
    metadata_obj,
    Column("faculty_id", INTEGER),
    Column("speciality_id", INTEGER),
    Column("university_id", INTEGER),
    Column("speciality_info", JSON),
)
