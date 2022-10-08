from models import bed_places, user, hostel, university, user_request

from sqlalchemy import (Column, INTEGER, DATETIME, ForeignKey, VARCHAR, FLOAT)
from sqlalchemy.orm import relationship

from db import Base


class UserRequestReview(Base):
    __tablename__ = "user_request_review"

    user_request_review_id = Column(INTEGER, primary_key=True)
    date_created = Column(DATETIME)
    room_number = Column(INTEGER)
    start_date_accommodation = Column(DATETIME)
    end_date_accommodation = Column(DATETIME)
    total_sum = Column(FLOAT)
    payment_deadline = Column(DATETIME)
    remark = Column(VARCHAR(length=255))
    date_review = Column(DATETIME)
    bed_place_id = Column(INTEGER, ForeignKey("bed_places.bed_place_id"))
    reviewer = Column(INTEGER, ForeignKey("user.user_id"))
    hostel_id = Column(INTEGER, ForeignKey("hostel.hostel_id"))
    university_id = Column(INTEGER, ForeignKey("university.university_id"))
    user_request_id = Column(INTEGER, ForeignKey("user_request.user_request_id"))

    bed_places = relationship("BedPlaces", back_populates='user_request_reviews')
    users = relationship("User", back_populates='reviewer')
    hostels = relationship("Hostel", back_populates='user_request_reviews')
    university = relationship("University", back_populates='user_request_reviews')
    user_request = relationship("UserRequest", back_populates='user_request_reviews')

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_review_id="{self.user_request_review_id}", university_id="{self.university_id}",' \
               f'user_request_id="{self.user_request_id}", date_created="{self.date_created}", reviewer="{self.reviewer}",' \
               f'hostel_id="{self.hostel_id}", room_number="{self.room_number}", start_date_accommodation="{self.start_date_accommodation}",' \
               f'end_date_accommodation="{self.end_date_accommodation}", total_sum="{self.total_sum}", payment_deadline="{self.payment_deadline}",' \
               f'remark="{self.remark}", date_review="{self.date_review}", bed_place_id="{self.bed_place_id}")'