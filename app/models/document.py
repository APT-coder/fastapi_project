from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.audit_mixin import AuditMixin
from app.models.enums import DocumentType, DocumentStatus


class Document(AuditMixin, Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False)
    file_identifier = Column(String, nullable=False, unique=True, index=True)

    document_type = Column(
        Enum(
            DocumentType,
            name="document_type",
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    status = Column(
        Enum(
            DocumentStatus,
            name="document_status",
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    # Relationships
    user = relationship("User", foreign_keys=[user_id], lazy="selectin")
    products = relationship("Product", back_populates="documents", lazy="selectin")
