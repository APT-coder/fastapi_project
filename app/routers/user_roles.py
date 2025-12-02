from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.api_response_schema import APIResponse
from app.services.user_role_service import assign_user_role
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead

router = APIRouter()

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

