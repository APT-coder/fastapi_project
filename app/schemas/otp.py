from pydantic import BaseModel, ConfigDict, EmailStr


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

model_config = ConfigDict(from_attributes=True)