from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True