from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import get_all_items, create_item

router = APIRouter()

@router.get("/", response_model=List[ItemRead])
async def read_items(db: AsyncSession = Depends(get_db)):
    items = await get_all_items(db)
    return [ItemRead.from_orm(i) for i in items]

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def post_item(item_in: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = await create_item(db, item_in)
    return ItemRead.from_orm(item)
