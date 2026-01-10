from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from typing import List, Optional
from app.services.email_service import send_email
from app.dependencies import security_optional

router = APIRouter()

@router.post("/send", dependencies=[Depends(security_optional)])
async def send_mail(
    recipients: List[str] = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    attachments: Optional[List[UploadFile]] = File(None),
):
    try:
        await send_email(
            recipients=recipients,
            subject=subject,
            body=body,
            attachments=attachments,
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
