from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    message: str  
    data: Optional[T] = None  

    model_config = ConfigDict(from_attributes=True)  
