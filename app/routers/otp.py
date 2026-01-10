from fastapi import APIRouter, BackgroundTasks
from app.schemas.otp import OTPRequest
from app.services.otp_service import generate_otp, save_otp
from app.services.email_service import send_otp_email

router = APIRouter()


@router.post("/send")
async def send_otp(request: OTPRequest, background_tasks: BackgroundTasks):
    otp = generate_otp()
    save_otp(request.email, otp)

    background_tasks.add_task(send_otp_email, request.email, otp)
    return {"message": "OTP sent successfully"}
