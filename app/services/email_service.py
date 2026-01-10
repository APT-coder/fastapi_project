from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import UploadFile
from typing import List, Optional
from app.core.email_config import email_conf

async def send_email(
    recipients: List[str],
    subject: str,
    body: str,
    attachments: Optional[List[UploadFile]] = None,
):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
        attachments=attachments,
    )

    fm = FastMail(email_conf)
    await fm.send_message(message)
