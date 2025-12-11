from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.enums import UserStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
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
