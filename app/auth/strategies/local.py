from sqlalchemy import or_, select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.provider_utils import has_provider
from app.auth.strategies.base import AuthStrategy
from app.models.user import User
from app.models.enums import AuthProvider, UserStatus
from app.core.security import verify_password
from app.services.helper_service import is_password_expired


class LocalAuthStrategy(AuthStrategy):

    async def authenticate(self, db: AsyncSession, data) -> User:
        result = await db.execute(
            select(User).where(
                or_(
                    User.username == data.identifier,
                    User.phone == data.identifier,
                    User.email == data.identifier,
                )
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
        
        if not has_provider(user, AuthProvider.local):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password login not enabled for this account",
            )   
            
        if not user.password or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if user.user_status == UserStatus.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is inactive",
            )

        if is_password_expired(user.password_updated_at):
            user.user_status = UserStatus.INACTIVE
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password expired",
            )

        return user
