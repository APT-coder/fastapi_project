from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin


class Role(AuditMixin, Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True, nullable=False)

    # Many-to-many with Permission
    permissions = relationship(
        "Permission",
        secondary="role_permission",
        back_populates="roles",
        lazy="selectin"
    )

    # Many-to-many with User
    users = relationship(
        "User",
        secondary="user_role",
        back_populates="roles",
        lazy="select"
    )