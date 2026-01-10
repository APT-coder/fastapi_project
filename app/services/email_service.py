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
    message_data = {
        "subject": subject,
        "recipients": recipients,
        "body": body,
        "subtype": MessageType.html,
    }

    if attachments:
        message_data["attachments"] = attachments

    message = MessageSchema(**message_data)

    fm = FastMail(email_conf)
    await fm.send_message(message)


async def send_otp_email(email: str, otp: str):
    subject = "Your verification OTP"
    body = f"""
    <p>Your OTP is <strong>{otp}</strong></p>
    <p>This OTP is valid for <b>5 minutes</b>.</p>
    """

    await send_email([email], subject, body)
