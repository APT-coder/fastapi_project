from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
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