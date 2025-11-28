from pydantic import BaseModel

class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int

class UserRoleRead(BaseModel):
    id: int
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
