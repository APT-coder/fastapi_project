from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin


class Category(AuditMixin, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # One-to-many: Category -> Products
    products = relationship("Product", back_populates="category")
