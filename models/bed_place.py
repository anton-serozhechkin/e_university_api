from models import user_request_review

from sqlalchemy import (Column, VARCHAR, INTEGER)
from sqlalchemy.orm import relationship

from db import Base


class BedPlace(Base):
    __tablename__ = 'bed_place'

    bed_place_id = Column(INTEGER, primary_key=True, nullable=False)
    bed_place_name = Column(VARCHAR(length=50), nullable=False)

    user_request_reviews = relationship("UserRequestReview", back_populates='bed_places')

    def __repr__(self):
        return f'{self.__class__.__name__}(bed_place_id="{self.bed_place_id}", bed_place_name="{self.bed_place_name}")'
