from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.services.user_role_service import assign_user_role
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead

router = APIRouter()

@router.post("/", response_model=UserRoleRead)
async def assign(data: UserRoleCreate, db: AsyncSession = Depends(get_db)):
    result = await assign_user_role(db, data)
    if not result:
        raise HTTPException(400, "User already has this role")
    return result
