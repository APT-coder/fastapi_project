from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.strategies.google import GoogleAuthStrategy
from app.auth.strategies.local import LocalAuthStrategy
from app.models.user import User
from app.core.security import create_access_token
from app.dependencies import get_db, get_current_user, security_optional
from app.schemas.user import GoogleLoginRequest, LoginRequest, LoginResponse, UserCreate, UserRead
from app.services.user_service import create_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    strategy = LocalAuthStrategy()
    user = await strategy.authenticate(db, request)

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return LoginResponse(
        access_token=access_token,
        user=UserRead.from_orm(user),
    )


@router.post("/login/google", response_model=LoginResponse)
async def google_login(
    request: GoogleLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    strategy = GoogleAuthStrategy()
    user = await strategy.authenticate(db, request)

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return LoginResponse(
        access_token=access_token,
        user=UserRead.from_orm(user),
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(security_optional)])
async def register_user(user_in: UserCreate, 
                        db: AsyncSession = Depends(get_db)):
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
        
    user = await create_user(db, user_in)
    return UserRead.from_orm(user)


@router.get("/me", response_model=UserRead)
async def test_current_user(
    current_user: User = Depends(get_current_user),
):
    return UserRead.from_orm(current_user)