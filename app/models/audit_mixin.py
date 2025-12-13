from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import declared_attr


class AuditMixin:
    created_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @declared_attr
    def created_by(cls):
        return Column(
            Integer,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True
        )

    @declared_attr
    def updated_by(cls):
        return Column(
            Integer,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True
        )
