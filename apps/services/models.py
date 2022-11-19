from apps.common.db import Base

from sqlalchemy import (
    MetaData, Column, Table, INTEGER, VARCHAR, ForeignKey, DATETIME, JSON, TIMESTAMP, DECIMAL
)
from sqlalchemy.orm import relationship


metadata_obj = MetaData()

STATUS_MAPPING = {"Схвалено": 1, "Відхилено": 2, "Розглядається": 3, "Скасовано": 4}


class Service(Base):
    __tablename__ = 'service'

    service_id = Column(INTEGER, primary_key=True, nullable=False)
    service_name = Column(VARCHAR(length=255), nullable=False)

    requisites = relationship("Requisites", back_populates="service")
    user_requests = relationship("UserRequest", back_populates="service")

    def __repr__(self):
        return f'{self.__class__.__name__}(service_id="{self.service_id}",service_name="{self.service_name}")'


class UserRequest(Base):
    __tablename__ = "user_request"

    user_request_id = Column(INTEGER, primary_key=True, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    comment = Column(VARCHAR(length=255))
    user_id = Column(INTEGER, ForeignKey("user.user_id"), nullable=False)
    service_id = Column(INTEGER, ForeignKey("service.service_id"), nullable=False)
    faculty_id = Column(INTEGER, ForeignKey("faculty.faculty_id"), nullable=False)
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    status_id = Column(INTEGER, ForeignKey("status.status_id"), nullable=False)

    user = relationship("User", back_populates="user_requests")
    service = relationship("Service", back_populates="user_requests")
    faculty = relationship("Faculty", back_populates="user_requests")
    university = relationship("University", back_populates="user_requests")
    status = relationship("Status", back_populates="user_requests")
    user_documents = relationship("UserDocument", back_populates="user_request")
    user_request_review = relationship("UserRequestReview", back_populates='user_request')

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_id="{self.user_request_id}",' \
               f'date_created="{self.date_created}", comment="{self.comment}",user_id="{self.user_id}", service_id="{self.service_id}",' \
               f'faculty_id="{self.faculty_id}", university_id="{self.university_id}", status_id="{self.status_id}")'


class Status(Base):
    __tablename__ = "status"

    status_id = Column(INTEGER, primary_key=True, nullable=False)
    status_name = Column(VARCHAR(length=50), nullable=False)

    user_requests = relationship("UserRequest", back_populates="status")

    def __repr__(self):
        return f'{self.__class__.__name__}(status_id="{self.status_id}",status_name="{self.status_name}")'


class Requisites(Base):
    __tablename__ = 'requisites'

    requisites_id = Column(INTEGER, primary_key=True, nullable=False)
    iban = Column(VARCHAR(length=100))
    organisation_code = Column(VARCHAR(length=50))
    payment_recognition = Column(VARCHAR(length=255))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    service_id = Column(INTEGER, ForeignKey("service.service_id"), nullable=False)

    university = relationship("University", back_populates="requisites")
    service = relationship("Service", back_populates="requisites")

    def __repr__(self):
        return f'{self.__class__.__name__}(requisites_id="{self.requisites_id}",iban="{self.iban}",organisation_code="{self.organisation_code}",' \
               f'payment_recognition="{self.payment_recognation}",university_id="{self.university_id}",service_id="{self.service_id}")'


class UserRequestReview(Base):
    __tablename__ = "user_request_review"
    user_request_review_id = Column(INTEGER, primary_key=True, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    room_number = Column(INTEGER)
    start_date_accommodation = Column(DATETIME)
    end_date_accommodation = Column(DATETIME)
    total_sum = Column(DECIMAL(7, 2))
    payment_deadline = Column(DATETIME)
    remark = Column(VARCHAR(length=255))
    bed_place_id = Column(INTEGER, ForeignKey("bed_place.bed_place_id"))
    reviewer = Column(INTEGER, ForeignKey("user.user_id"), nullable=False)  # TODO: rename column to reviewer_id
    hostel_id = Column(INTEGER, ForeignKey("hostel.hostel_id"))
    university_id = Column(INTEGER, ForeignKey("university.university_id"), nullable=False)
    user_request_id = Column(INTEGER, ForeignKey("user_request.user_request_id"), nullable=False)

    bed_place = relationship("BedPlace", back_populates='user_request_review')
    reviewer_user = relationship("User", back_populates='user_request_reviews')  # TODO: rename to reviewer
    hostel = relationship("Hostel", back_populates='user_request_reviews')
    university = relationship("University", back_populates='user_request_reviews')
    user_request = relationship("UserRequest", back_populates='user_request_review')

    def __repr__(self):
        return f'{self.__class__.__name__}(user_request_review_id="{self.user_request_review_id}",date_created="{self.date_created}",' \
               f'room_number="{self.room_number}", start_date_accommodation="{self.start_date_accommodation}",end_date_accommodation="{self.end_date_accommodation}", total_sum="{self.total_sum}", payment_deadline="{self.payment_deadline}",' \
               f'remark="{self.remark}", bed_place_id="{self.bed_place_id}",reviewer="{self.reviewer}",hostel_id="{self.hostel_id}",university_id="{self.university_id}",user_request_id="{self.user_request_id}")'


class UserDocument(Base):
    __tablename__ = "user_document"

    user_document_id = Column(INTEGER, primary_key=True, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    content = Column(VARCHAR(length=255), nullable=False)
    user_request_id = Column(INTEGER, ForeignKey("user_request.user_request_id"), nullable=False)

    user_request = relationship("UserRequest", back_populates="user_documents")

    def __repr__(self):
        return f'{self.__class__.__name__}(user_document_id="{self.user_document_id}", date_created="{self.date_created}", ' \
               f'name="{self.name}", content="{self.content}", user_request_id="{self.user_request_id}")'


user_request_booking_hostel_view = Table('user_request_booking_hostel_view', metadata_obj,
                                         Column('full_name', JSON),
                                         Column('user_id', INTEGER),
                                         Column('faculty_name', VARCHAR(255)),
                                         Column('university_id', INTEGER),
                                         Column('short_university_name', VARCHAR(50)),
                                         Column('rector_full_name', JSON),
                                         Column('speciality_code', INTEGER),
                                         Column('speciality_name', VARCHAR(255)),
                                         Column('course', INTEGER),
                                         Column('educ_level', VARCHAR(1)),
                                         Column('date_today', DATETIME),
                                         Column('start_year', INTEGER),
                                         Column('finish_year', INTEGER),
                                         Column('gender', VARCHAR(1)))


user_request_details_view = Table('user_request_details_view', metadata_obj,
                                  Column('user_request_id', INTEGER),
                                  Column('university_id', INTEGER),
                                  Column('date_created', DATETIME),
                                  Column('service_name', VARCHAR(255)),
                                  Column('status_name', VARCHAR(50)),
                                  Column('status_id', INTEGER),
                                  Column('comment', VARCHAR(255)),
                                  Column('hostel_name', JSON),
                                  Column('room_number', INTEGER),
                                  Column('bed_place_name', VARCHAR(50)),
                                  Column('remark', VARCHAR(255)),
                                  Column('documents', JSON))


user_request_exist_view = Table('user_request_exist_view', metadata_obj,
                                Column('user_request_id', INTEGER),
                                Column('user_id', INTEGER),
                                Column('faculty_id', INTEGER),
                                Column('university_id', INTEGER),
                                Column('service_id', INTEGER),
                                Column('status', JSON))


user_request_list_view = Table('user_request_list_view', metadata_obj,
                               Column('university_id', INTEGER),
                               Column('user_id', INTEGER),
                               Column('user_request_id', INTEGER),
                               Column('service_name', VARCHAR(255)),
                               Column('status', JSON),
                               Column('date_created', DATETIME))


hostel_accommodation_view = Table('hostel_accommodation_view', metadata_obj,
                                  Column('university_id', INTEGER),
                                  Column('user_request_review_id', INTEGER),
                                  Column('user_request_id', INTEGER),
                                  Column('hostel_name', JSON),
                                  Column('hostel_address', JSON),
                                  Column('room_number', INTEGER),
                                  Column('bed_place_name', VARCHAR(50)),
                                  Column('month_price', DECIMAL(6, 2)),
                                  Column('start_date_accommodation', TIMESTAMP),
                                  Column('end_date_accommodation', TIMESTAMP),
                                  Column('total_sum', DECIMAL(7, 2)),
                                  Column('iban', VARCHAR(100)),
                                  Column('university_name', VARCHAR(255)),
                                  Column('organisation_code', VARCHAR(50)),
                                  Column('payment_recognation', VARCHAR(255)),
                                  Column('commandant_full_name', JSON),
                                  Column('telephone_number', VARCHAR(50)),
                                  Column('documents', JSON))

user_document_view = Table('user_document_view', metadata_obj,
                           Column('university_id', INTEGER),
                           Column('student_id', INTEGER),
                           Column('user_document_id', INTEGER),
                           Column('name', VARCHAR(255)),
                           Column('date_created', DATETIME))

