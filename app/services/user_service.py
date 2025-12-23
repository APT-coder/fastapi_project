from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.provider_utils import has_provider
from app.core.security import verify_password
from app.models.enums import AuthProvider, UserStatus
from app.models.user import User
from app.schemas.user import UserCreate, UserStatusUpdate

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_password = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        phone=user_in.phone,
        email=user_in.email,
        password=hashed_password,
        password_updated_at=datetime.now(timezone.utc),
        user_status=UserStatus.PENDING.value,
        auth_providers=AuthProvider.local.value
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_status(db: AsyncSession, user_id: int, status_update: UserStatusUpdate):
    # Fetch user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    
    # Update status
    if user.user_status != status_update.user_status:
        user.user_status = status_update.user_status

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
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Block non-local users
    if not has_provider(user, AuthProvider.local):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password change not allowed for this account",
        )

    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No password set for this account",
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

    if user.user_status == UserStatus.INACTIVE:
        user.user_status = UserStatus.ACTIVE

    await db.commit()
    await db.refresh(user)

    return {"message": "Password updated successfully"}