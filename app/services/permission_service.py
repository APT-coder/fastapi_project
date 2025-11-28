from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.permission import Permission
from app.schemas.permission_schema import PermissionCreate

async def create_permission(db: AsyncSession, data: PermissionCreate):
    # check duplicate
    exists = await db.execute(
        select(Permission).where(Permission.permission_name == data.permission_name)
    )
    if exists.scalar_one_or_none():
        return None

    permission = Permission(permission_name=data.permission_name)
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission

async def get_permissions(db: AsyncSession):
    result = await db.execute(select(Permission))
    return result.scalars().all()
