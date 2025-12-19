from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document


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
