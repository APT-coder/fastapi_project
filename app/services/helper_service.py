from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.user import User


async def get_user_with_roles(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User)
        .filter(User.id == user_id)
        .options(
            selectinload(User.roles)
            .selectinload(Role.permissions)
        )
    )
    return result.scalar_one()
