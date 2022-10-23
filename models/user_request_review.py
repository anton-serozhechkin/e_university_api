from models import bed_place, user, hostel, university, user_request

from sqlalchemy import (Column, INTEGER, DATETIME, ForeignKey, VARCHAR, FLOAT)
from sqlalchemy.orm import relationship

from db import Base


class UserRequestReview(Base):
    __tablename__ = "user_request_review"
    user_request_review_id = Column(INTEGER, primary_key=True, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    room_number = Column(INTEGER)
    start_date_accommodation = Column(DATETIME)
    end_date_accommodation = Column(DATETIME)
    total_sum = Column(FLOAT)
    payment_deadline = Column(DATETIME)
    remark = Column(VARCHAR(length=255))
    date_review = Column(DATETIME, nullable=False)
    bed_place_id = Column(INTEGER, ForeignKey("bed_place.bed_place_id"))
    reviewer = Column(INTEGER, ForeignKey("user.user_id"), nullable=False)
    hostel_id = Column(INTEGER, ForeignKey("hostel.hostel_id"))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    user_request_id = Column(INTEGER, ForeignKey("user_request.user_request_id"), nullable=False)

    bed_place = relationship("BedPlace", back_populates='user_request_reviews')
    reviewer_user = relationship("User", back_populates='user_request_reviews')
    hostels = relationship("Hostel", back_populates='user_request_reviews')
    university = relationship("University", back_populates='user_request_reviews')
    user_request = relationship("UserRequest", back_populates='user_request_reviews')

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_review_id="{self.user_request_review_id}",date_created="{self.date_created}",' \
               f'room_number="{self.room_number}", start_date_accommodation="{self.start_date_accommodation}",end_date_accommodation="{self.end_date_accommodation}", total_sum="{self.total_sum}", payment_deadline="{self.payment_deadline}",' \
               f'remark="{self.remark}", date_review="{self.date_review}", bed_place_id="{self.bed_place_id}",reviewer="{self.reviewer}",hostel_id="{self.hostel_id}",university_id="{self.university_id}",user_request_id="{self.user_request_id}")'