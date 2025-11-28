from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_role import UserRole
from app.schemas.user_role_schema import UserRoleCreate

async def assign_user_role(db: AsyncSession, data: UserRoleCreate):
    exists = await db.execute(
        select(UserRole).where(
            UserRole.user_id == data.user_id,
            UserRole.role_id == data.role_id
        )
    )

    if exists.scalar_one_or_none():
        return None

    user_role = UserRole(user_id=data.user_id, role_id=data.role_id)
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    return user_role
