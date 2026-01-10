from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import DocumentType, DocumentStatus


class DocumentCreate(BaseModel):
    document_name: str
    file_identifier: str
    document_type: DocumentType
    status: DocumentStatus
    user_id: int
    product_id: int

    
class DocumentRead(BaseModel):
    document_id: int
    document_name: str
    file_identifier: str
    document_type: DocumentType
    status: DocumentStatus
    user_id: int
    product_id: int
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)
