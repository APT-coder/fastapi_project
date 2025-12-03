from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.dependencies import get_db
from app.models.user import User
from app.schemas.api_response_schema import APIResponse
from app.schemas.user import UserCreate, UserRead
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead
from app.services.helper_service import get_user_with_roles
from app.services.user_role_service import assign_user_role
from app.services.user_service import get_all_users, create_user

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return [UserRead.from_orm(u) for u in users]

@router.get("/{user_id}", response_model=UserRoleRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_with_roles(db, user_id)
    return UserRoleRead.from_orm(user)

@router.post("/assign-roles/{user_id}", response_model=APIResponse[UserRoleRead])
async def assign(user_id: int, data: UserRoleCreate, db: AsyncSession = Depends(get_db)):

    try:
        data.user_id = user_id
        result = await assign_user_role(db, data)

        return APIResponse(
            message=result["message"],
            data=result["user"]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
