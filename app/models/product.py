from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base


class Product(Base):
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
    seller = relationship("User", backref="products")
    category = relationship("Category", back_populates="products")
