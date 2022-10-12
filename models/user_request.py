from datetime import datetime

from models import user_document, user_request_review

from sqlalchemy import (Column, INTEGER, VARCHAR, ForeignKey, DateTime)
from sqlalchemy.orm import relationship

from db import Base

class UserRequest(Base):
    __tablename__ = "user_request"

    user_request_id = Column(INTEGER, primary_key=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    comment = Column(VARCHAR(length=255))
    user_id = Column(INTEGER, ForeignKey("user.user_id"))
    service_id = Column(INTEGER, ForeignKey("service.service_id"))
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"))
    university_id = Column(INTEGER, ForeignKey("university.university_id"))
    status_id = Column(INTEGER, ForeignKey("status.status_id"))

    users = relationship("User", back_populates="user_request")
    service = relationship("Service", back_populates="user_request")
    faculties = relationship("Faculty", back_populates="user_request")
    university = relationship("University", back_populates="user_request")
    status = relationship("Status", back_populates="user_request")
    user_documents = relationship("UserDocument", back_populates="user_request")
    user_request_reviews = relationship("UserRequestReview", back_populates='user_request')

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_id="{self.user_request_id}",' \
               f'date_created="{self.date_created}", comment="{self.comment}",user_id="{self.user_id}", service_id="{self.service_id}",' \
               f'faculty_id="{self.faculty_id}", university_id="{self.university_id}", status_id="{self.status_id}")'