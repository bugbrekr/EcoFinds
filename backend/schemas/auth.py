from pydantic import BaseModel

class OTPRequest(BaseModel):
    phone_number: str

class OTPValidationRequest(BaseModel):
    session_id: str
    otp: str

class LoginEmailRequest(BaseModel):
    email: str

class LoginPasswordRequest(BaseModel):
    email: str
    password: str

class LoginRegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str