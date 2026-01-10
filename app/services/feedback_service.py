from sqlalchemy.ext.asyncio import AsyncSession
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate
from app.services.email_service import send_email  

async def add_feedback(db: AsyncSession, feedback_in: FeedbackCreate):
    feedback = Feedback(**feedback_in.dict())
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)

    # Send thank you email
    subject = "Thank you for your feedback"
    body = f"Hi {feedback.name},<br><br>Thank you for your feedback!<br><br>Your Rating: {feedback.rating}<br>Comments: {feedback.description or 'None'}"
    await send_email([feedback.email], subject, body)

    return feedback
