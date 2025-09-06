from pydantic import BaseModel

class OTPRequest(BaseModel):
    phone_number: str

class OTPValidationRequest(BaseModel):
    session_id: str
    otp: str