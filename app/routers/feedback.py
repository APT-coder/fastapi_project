from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.feedback import FeedbackCreate, FeedbackRead
from app.services.feedback_service import add_feedback
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback_in: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await add_feedback(db, feedback_in)
