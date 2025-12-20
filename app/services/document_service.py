from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document
from app.schemas.document import DocumentCreate


async def get_document_by_id(db: AsyncSession, document_id: int) -> Document | None:
    result = await db.execute(
        select(Document).where(Document.document_id == document_id)
    )
    return result.scalar_one_or_none()


async def get_documents_by_product_id(
    db: AsyncSession, product_id: int
) -> list[Document]:
    result = await db.execute(
        select(Document).where(Document.product_id == product_id)
    )
    return result.scalars().all()


async def create_document(
    db: AsyncSession, document_in: DocumentCreate
) -> Document:
    document = Document(
        document_name=document_in.document_name,
        file_identifier=document_in.file_identifier,
        document_type=document_in.document_type,
        status=document_in.status,
        user_id=document_in.user_id,
        product_id=document_in.product_id
    )

    db.add(document)

    try:
        await db.commit()
        await db.refresh(document)
    except IntegrityError:
        await db.rollback()
        raise

    return document
