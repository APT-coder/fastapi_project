from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.dependencies import get_db
from app.schemas.user import LoginRequest, LoginResponse, UserRead

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.execute(
        select(User).where(User.phone == request.phone)
    )
    user = user.scalar_one_or_none()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.phone})

    return LoginResponse(
        access_token=access_token,
        user=UserRead.from_orm(user)
    )
