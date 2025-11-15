from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_in: UserCreate):
    user = User(username=user_in.username, full_name=user_in.full_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user