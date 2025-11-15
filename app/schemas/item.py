from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    owner_id: Optional[int] = None

class ItemRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: Optional[int]

    class Config:
        orm_mode = True