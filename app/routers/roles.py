from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.api_response_schema import APIResponse
from app.services.role_service import create_or_update_role, get_roles
from app.schemas.role_schema import RoleCreate, RoleRead

router = APIRouter()

@router.post("/", response_model=APIResponse[RoleRead])
async def create_or_update(data: RoleCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await create_or_update_role(db, data)
        
        return APIResponse(
            message=result["message"],
            data=result["role"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[RoleRead])
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await get_roles(db)

