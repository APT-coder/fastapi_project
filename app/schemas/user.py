from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.models.enums import UserStatus


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
    user_status: str
    created_date: datetime
    updated_date: datetime

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