from models import user, faculty

from sqlalchemy import (Column, INTEGER, ForeignKey)
from sqlalchemy.orm import relationship

from db import Base


class UserFaculty(Base):
    __tablename__ = "user_faculty"

    user_id = Column(INTEGER, ForeignKey("user.user_id"), nullable=False, primary_key=True)
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"), nullable=False, primary_key=True)

    users = relationship("User", back_populates="user_faculty")
    faculties = relationship("Faculty", back_populates="faculty")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id="{self.user_id}", faculty_id="{self.faculty_id}")'
