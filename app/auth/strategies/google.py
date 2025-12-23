from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth.provider_utils import add_provider, has_provider
from app.auth.strategies.base import AuthStrategy
from app.core.google_auth import verify_google_token
from app.models.user import User
from app.models.enums import AuthProvider, UserStatus


class GoogleAuthStrategy(AuthStrategy):

    async def authenticate(self, db: AsyncSession, data) -> User:
        google_user = verify_google_token(data.token)

        if not google_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

        email = google_user.get("email")
        name = google_user.get("name")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google account has no email",
            )

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                username=email.split("@")[0],
                email=email,
                full_name=name,
                auth_providers="google",
                user_status=UserStatus.ACTIVE,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        else:
            if not has_provider(user, AuthProvider.google):
                add_provider(user, AuthProvider.google)
                await db.commit()
                await db.refresh(user)

        if user.user_status == UserStatus.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account inactive",
            )

        return user
