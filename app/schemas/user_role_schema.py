from typing import List
from pydantic import BaseModel, ConfigDict

from app.schemas.role_schema import RoleRead
from app.schemas.user import UserRead

class UserRoleCreate(BaseModel):
    user_id: int | None = None
    role_ids: List[int]
    
class UserRoleRead(UserRead):
    roles: List[RoleRead]

    model_config = ConfigDict(from_attributes=True)
