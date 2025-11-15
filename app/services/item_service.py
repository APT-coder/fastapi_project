from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate

async def get_all_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def create_item(db: AsyncSession, item_in: ItemCreate):
    item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=item_in.owner_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item