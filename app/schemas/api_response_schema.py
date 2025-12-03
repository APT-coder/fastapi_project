from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(Generic[T], BaseModel):
    message: str  
    data: Optional[T] = None  

    class Config:
        orm_mode = True  
