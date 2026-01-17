from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_db
from app.schemas.user_preferences import (
    UserPreferencesCreateUpdate,
    UserPreferencesRead
)
from app.services.user_preferences_service import (
    get_user_preferences,
    create_or_update_preferences
)

router = APIRouter()

@router.get("/{user_id}", response_model=UserPreferencesRead)
async def get_preferences(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    prefs = await get_user_preferences(db, user_id)

    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")

    return prefs


@router.post("/{user_id}", response_model=UserPreferencesRead)
async def create_or_update(
    user_id: int,
    payload: UserPreferencesCreateUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    prefs = await create_or_update_preferences(db, user_id, payload)
    return prefs
