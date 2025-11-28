from pydantic import BaseModel

class PermissionBase(BaseModel):
    permission_name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int

    class Config:
        orm_mode = True
