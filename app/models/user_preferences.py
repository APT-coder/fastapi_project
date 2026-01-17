from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    display_name = Column(String(100), nullable=True)
    email_notification_enabled = Column(Boolean, default=True)
    profile_pic_link = Column(String, nullable=True)

    user = relationship("User", backref="preferences")
