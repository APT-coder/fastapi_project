from typing import List
from pydantic import BaseModel

from app.schemas.role_schema import RoleRead
from app.schemas.user import UserRead

class UserRoleCreate(BaseModel):
    user_id: int | None = None
    role_ids: List[int]
    
class UserRoleRead(UserRead):
    roles: List[RoleRead]

    class Config:
        orm_mode = True
