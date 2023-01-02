from sqlalchemy import INTEGER, VARCHAR, Column, ForeignKey, func
from sqlalchemy.orm import relationship

from apps.common.db import Base
from apps.common.utils import AwareDateTime


class Role(Base):
    __tablename__ = "role"

    role_id = Column(INTEGER, primary_key=True)
    role_name = Column(VARCHAR(length=50))
    created_at = Column(AwareDateTime, default=func.now(), nullable=False)
    updated_at = Column(AwareDateTime, default=func.now(), nullable=False)

    actions = relationship("Action", back_populates="roles")
    users = relationship("User", back_populates="roles")

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}(role_id="{self.role_id}",'
            f' role_name="{self.role_name}")'
        )


class Action(Base):
    __tablename__ = "action"

    action_id = Column(INTEGER, primary_key=True, nullable=False)
    action_name = Column(VARCHAR(length=50), nullable=False)
    role_id = Column(INTEGER, ForeignKey("role.role_id"), nullable=False)

    roles = relationship("Role", back_populates="actions")

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(action_id="{self.action_id}",'
            f' action_name="{self.action_name}",role_id="{self.role_id}")'
        )
