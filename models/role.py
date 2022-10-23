from models import action

from sqlalchemy import (Column, INTEGER, VARCHAR)
from sqlalchemy.orm import relationship

from db import Base


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER, primary_key=True)
    role_name = Column(VARCHAR(length=50))

    actions = relationship('Action', back_populates='roles')
    users = relationship('User', back_populates='roles')

    def __str__(self):
        return f'{self.__class__.__name__}(role_id="{self.role_id}",role_name="{self.role_name}")'
