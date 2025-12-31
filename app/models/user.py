from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin
from app.models.enums import AuthProvider, UserStatus


class User(AuditMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    auth_providers = Column(String, nullable=False, default=AuthProvider.local.value)
    password_updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user_status = Column(
        Enum(UserStatus, name="userstatus", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        server_default=UserStatus.PENDING.value)

    # Many-to-many with Role
    roles = relationship(
        "Role",
        secondary="user_role",
        back_populates="users",
        lazy="selectin"
    )
