from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_preferences import UserPreferences


async def get_user_preferences(db: AsyncSession, user_id: int) -> UserPreferences | None:
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_or_update_preferences(
    db: AsyncSession,
    user_id: int,
    data
) -> UserPreferences:
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user_id)
    )
    prefs = result.scalar_one_or_none()

    if prefs:
        # update
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(prefs, field, value)
    else:
        # create
        prefs = UserPreferences(
            user_id=user_id,
            **data.model_dump()
        )
        db.add(prefs)

    await db.commit()
    await db.refresh(prefs)
    return prefs
