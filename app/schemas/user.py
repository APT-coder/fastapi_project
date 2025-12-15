from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.models.enums import UserStatus


class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    phone: str
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRead(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    user_status: str
    created_date: datetime
    updated_date: datetime
    password_updated_at: datetime
    created_by: int | None
    updated_by: int | None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    identifier: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class UserStatusUpdate(BaseModel):
    user_status: UserStatus

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
