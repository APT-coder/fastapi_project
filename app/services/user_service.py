from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from app.models.enums import UserStatus
from app.models.user import User
from app.schemas.user import UserCreate, UserStatusUpdate

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(db: AsyncSession, user_in: UserCreate, created_by: int | None = None):
    hashed_password = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        phone=user_in.phone,
        email=user_in.email,
        password=hashed_password,
        password_updated_at=datetime.now(timezone.utc),
        user_status=UserStatus.PENDING.value,
        created_by=created_by,
        updated_by=created_by,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_status(db: AsyncSession, user_id: int, status_update: UserStatusUpdate, current_user: User):
    # Fetch user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    
    # Update status
    if user.user_status != status_update.user_status:
        user.user_status = status_update.user_status
        user.updated_by = current_user.id

    await db.commit()
    await db.refresh(user)

    return {
        "message": f"User {user_id} status updated to '{status_update.user_status}'.",
        "user": user
    }

async def change_user_password(
    db: AsyncSession,
    user_id: int,
    old_password: str,
    new_password: str,
    current_user_id: int,
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    if verify_password(new_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from old password",
        )

    user.password = hash_password(new_password)
    user.password_updated_at = datetime.now(timezone.utc)
    user.updated_by = current_user_id

    if user.user_status == UserStatus.INACTIVE:
        user.user_status = UserStatus.ACTIVE

    await db.commit()
    await db.refresh(user)

    return {"message": "Password updated successfully"}