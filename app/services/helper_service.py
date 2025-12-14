from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.user import User

PASSWORD_EXPIRY_DAYS = 60

def is_password_expired(password_updated_at: datetime) -> bool:
    if not password_updated_at:
        return False

    now = datetime.now(timezone.utc)  
    return now - password_updated_at > timedelta(days=PASSWORD_EXPIRY_DAYS)

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
