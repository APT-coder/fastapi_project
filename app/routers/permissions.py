from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, security_optional
from app.services.permission_service import create_permission, get_permissions
from app.schemas.permission_schema import PermissionRead, PermissionCreate

router = APIRouter()

@router.post("/", response_model=PermissionRead,
             dependencies=[Depends(security_optional)])
async def create(data: PermissionCreate, db: AsyncSession = Depends(get_db)):
    result = await create_permission(db, data)
    if not result:
        raise HTTPException(400, "Permission already exists")
    return result

@router.get("/", response_model=list[PermissionRead])
async def list_permissions(db: AsyncSession = Depends(get_db)):
    return await get_permissions(db)
