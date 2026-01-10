from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.permission_schema import PermissionRead

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    permissions: Optional[List[int]] = []  # list of permission IDs

class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead]

    model_config = ConfigDict(from_attributes=True)
