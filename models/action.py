from models import role

from sqlalchemy import (Column, ForeignKey, VARCHAR, INTEGER)
from sqlalchemy.orm import relationship

from db import Base


class Action(Base):
    __tablename__ = 'action'

    action_id = Column(INTEGER, primary_key=True, nullable=False)
    action_name = Column(VARCHAR(length=50), nullable=False)
    role_id = Column(INTEGER, ForeignKey("role.role_id"), nullable=False)

    roles = relationship("Role", back_populates="actions")

    def __repr__(self):
        return (f'{self.__class__.__name__}(action_id="{self.action_id}",action_name="{self.action_name}", '
                f'role_id="{self.role_id}")')

