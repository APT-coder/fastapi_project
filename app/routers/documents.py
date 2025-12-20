from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.document import DocumentCreate, DocumentRead
from app.services.document_service import (
    create_document,
    get_document_by_id,
    get_documents_by_product_id,
)


router = APIRouter()


@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def save_document(
    document_in: DocumentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        document = await create_document(db, document_in)
        return DocumentRead.from_orm(document)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document with this file_identifier already exists",
        )
    

@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
    document = await get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return DocumentRead.from_orm(document)


@router.get("/get-by-product/{product_id}", response_model=List[DocumentRead])
async def get_documents_by_product(
    product_id: int, db: AsyncSession = Depends(get_db)
):
    documents = await get_documents_by_product_id(db, product_id)
    return [DocumentRead.from_orm(doc) for doc in documents]
