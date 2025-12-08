from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    phone: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    identifier: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
