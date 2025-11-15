from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import get_all_users, create_user

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    # convert ORM objects to pydantic models using from_orm
    return [UserRead.from_orm(u) for u in users]

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def post_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # uniqueness check
    existing = await db.execute(select(User).where(User.username == user_in.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username exists")
    user = await create_user(db, user_in)
    return UserRead.from_orm(user)
