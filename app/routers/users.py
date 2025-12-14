from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.api_response_schema import APIResponse
from app.schemas.user import UserRead, UserStatusUpdate
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead
from app.services.helper_service import get_user_with_roles
from app.services.user_role_service import assign_user_role
from app.services.user_service import get_all_users, update_user_status

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return [UserRead.from_orm(u) for u in users]

@router.get("/{user_id}", response_model=UserRoleRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(or_(User.id == user_id)))
    
    if not user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User Id"
        )
    
    user_roles = await get_user_with_roles(db, user_id)
    return UserRoleRead.from_orm(user_roles)

@router.post("/assign-roles/{user_id}", response_model=APIResponse[UserRoleRead])
async def assign(user_id: int, data: UserRoleCreate, db: AsyncSession = Depends(get_db)):

    try:
        data.user_id = user_id
        result = await assign_user_role(db, data)

        return APIResponse(
            message=result["message"],
            data=UserRoleRead.from_orm(result["user"])
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/status", response_model=APIResponse[UserRoleRead])
async def update_user_status_by_id(
    user_id: int,
    status_update: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = await update_user_status(db, user_id, status_update, current_user)

        return APIResponse(
            message=result["message"],
            data=UserRoleRead.from_orm(result["user"])
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
