from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available_count: int
    seller_id: int

    category_id: Optional[int] = None
    category_name: Optional[str] = None
    category_description: Optional[str] = None


class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    available_count: int
    seller_id: int
    category_id: int
    category_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
