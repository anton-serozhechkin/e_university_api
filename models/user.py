from models import student, user_request_review, user_faculty

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, BOOLEAN, TIMESTAMP)
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(INTEGER, primary_key=True, nullable=False)
    login = Column(VARCHAR(length=50), nullable=False, unique=True)
    password = Column(VARCHAR(length=50), nullable=False)
    last_visit = Column(TIMESTAMP)
    email = Column(VARCHAR(length=100), nullable=False, unique=True)
    is_active = Column(BOOLEAN, default=False)
    role_id = Column(INTEGER, ForeignKey("role.role_id"), nullable=True)

    student = relationship("Student", back_populates="users")
    user_request_reviews = relationship("UserRequestReview", back_populates="reviewer_user")
    user_faculty = relationship("UserFaculty", back_populates="users")
    user_request = relationship("UserRequest", back_populates="users")
    roles = relationship("Role", back_populates="users")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id="{self.user_id}", login="{self.login}", password="{self.password}", ' \
               f'last_visit="{self.last_visit}", email="{self.email}", is_active="{self.is_active}", role_id="{self.role_id}")'