from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enums import UserStatus
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.dependencies import get_db, get_current_user
from app.schemas.user import LoginRequest, LoginResponse, UserCreate, UserRead
from app.services.user_service import create_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(
            or_(
                User.username == request.identifier,
                User.phone == request.identifier,
                User.email == request.identifier
            )
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if user.user_status == UserStatus.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive. Please contact support."
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

    return LoginResponse(
        access_token=access_token,
        user=UserRead.from_orm(user)
    )

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, 
                        db: AsyncSession = Depends(get_db), 
                        current_user: User = Depends(get_current_user)):
    # Uniqueness check for username with phone or email whichever is provided
    existing = await db.execute(
        select(User).where(
            or_(
                User.username == user_in.username,
                User.phone == user_in.phone,
                User.email == user_in.email if user_in.email else False
            )
        )
    )
    
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = await create_user(db, user_in, current_user.id)
    return UserRead.from_orm(user)

@router.get("/me", response_model=UserRead)
async def test_current_user(
    current_user: User = Depends(get_current_user),
):
    return UserRead.from_orm(current_user)