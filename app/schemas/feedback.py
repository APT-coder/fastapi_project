from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, Optional

class FeedbackCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    rating: Annotated[int, Field(ge=1, le=5)]
    description: Optional[Annotated[str, Field(max_length=500)]] = None  # optional
    email: EmailStr

class FeedbackRead(FeedbackCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
