"""
Main backend server code.
Author: github.com/bugbrekr
Date: 31/08/2025
"""

import core.auth
import core.config
import core.database
import schemas.auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

config = core.config.load_config()

db = core.database.factory(
    uri=config.mongodb.uri,
    db_name=config.mongodb.db
)
twilioc = core.auth.TwilioClient(
    account_sid=config.twilio.account_sid,
    auth_token=config.twilio.auth_token,
    sms_from_ph=config.twilio.sms_from_ph
)

authorization_manager = core.auth.AuthorizationManager(
    config=config.auth,
    db=db,
    twilio_client=twilioc,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/a/auth/generateOTP")
def auth_generate_otp(otp_request: schemas.auth.OTPRequest):
    """
    Generates and sends OTP to user's phone number.
    """
    otp_session = authorization_manager.otp_factory(
        phone_number=otp_request.phone_number
    )
    session_id = otp_session.send_otp()
    return {
        "success": True,
        "code": 200,
        "session_id": session_id
    }

@app.post("/a/auth/verifyOTP")
def auth_login(otp_validation_request: schemas.auth.OTPValidationRequest):
    """
    Verifies OTP for the session.
    """
    otp_session = authorization_manager.otp_factory(
        session_id=otp_validation_request.session_id
    )
    res, res_code = otp_session.verify_otp(otp_validation_request.otp)
    return {
        "success": res,
        "code": res_code,
        "auth_token": "helloworld"
    }
