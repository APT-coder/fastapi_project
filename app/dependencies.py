from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import decode_access_token
from app.db.database import get_async_db


security_required = HTTPBearer(auto_error=True)
security_optional = HTTPBearer(auto_error=False)


async def get_db(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    auth_header = request.headers.get("Authorization")
    credentials = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token,
        )

    current_user = await _get_user_from_token(
        credentials=credentials,
        db=db,
        required=False,
    )

    db.sync_session.info["current_user_id"] = (
        current_user.id if current_user else None
    )

    return db


async def _get_user_from_token(
    credentials: HTTPAuthorizationCredentials | None,
    db: AsyncSession,
    required: bool,
) -> User | None:

    if credentials is None:
        if required:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return None

    payload = decode_access_token(credentials.credentials)

    if not payload or "user_id" not in payload:
        if required:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        return None

    result = await db.execute(
        select(User).where(User.id == payload["user_id"])
    )
    user = result.scalar_one_or_none()

    if not user and required:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_required),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    return await _get_user_from_token(credentials, db, required=True)


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_optional),
    db: AsyncSession = Depends(get_async_db),
) -> User | None:
    return await _get_user_from_token(credentials, db, required=False)


async def get_current_user_id(
    current_user: User = Depends(get_current_user),
) -> int:
    return current_user.id
