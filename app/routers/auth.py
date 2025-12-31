from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.strategies.google import GoogleAuthStrategy
from app.auth.strategies.local import LocalAuthStrategy
from app.auth.token_service import issue_login_response
from app.core.config import settings
from app.core.google_auth import exchange_code_for_token
from app.models.user import User
from app.dependencies import get_db, get_current_user, security_optional
from app.schemas.user import GoogleLoginRequest, LoginRequest, LoginResponse, UserCreate, UserRead
from app.services.user_service import create_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await LocalAuthStrategy().authenticate(db, request)
    return issue_login_response(user)


@router.get("/login/google/url")
async def get_google_login_url():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    url = f"{settings.GOOGLE_AUTH_BASE_URL}?{urlencode(params)}"
    return {"url": url}


@router.post("/login/google", response_model=LoginResponse)
async def google_login(
    request: GoogleLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await GoogleAuthStrategy().authenticate(db, request)
    return issue_login_response(user)


@router.get("/login/google/callback", response_model=LoginResponse)
async def google_login_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    token_response = await exchange_code_for_token(code)
    id_token = token_response.get("id_token")

    if not id_token:
        raise HTTPException(status_code=400, detail="No id_token returned")

    user = await GoogleAuthStrategy().authenticate(
        db,
        data=type("Obj", (), {"token": id_token})()
    )

    return issue_login_response(user)


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