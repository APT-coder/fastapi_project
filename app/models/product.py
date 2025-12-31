from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin


class Product(AuditMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    price = Column(Float, nullable=False)
    available_count = Column(Integer, nullable=False, default=0)

    # Foreign Keys
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Relationships
    seller = relationship(
        "User",
        foreign_keys=[seller_id],
        backref="products",
    )
    category = relationship("Category", back_populates="products")
    documents = relationship("Document", back_populates="products")
