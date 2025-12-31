from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin


class Permission(AuditMixin, Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, unique=True, index=True, nullable=False)

    # Many-to-many with Role (via role_permission)
    roles = relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions",
        lazy="selectin"
    )