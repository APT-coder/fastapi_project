from datetime import datetime
from pydantic import BaseModel
from app.models.enums import DocumentType, DocumentStatus


class DocumentRead(BaseModel):
    document_id: int
    document_name: str
    file_identifier: str
    document_type: DocumentType
    status: DocumentStatus
    user_id: int
    product_id: int
    created_date: datetime

    class Config:
        orm_mode = True
