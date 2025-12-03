from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate

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
        password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user