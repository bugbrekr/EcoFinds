"""
Main backend server code.
Author: github.com/bugbrekr
Date: 31/08/2025
"""

from typing import Annotated
import core.auth
import core.config
import core.database
import core.profile
import schemas.auth
from fastapi import FastAPI, Header
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

profile_manager = core.profile.ProfileManager(db=db)

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
def auth_verify_otp(otp_validation_request: schemas.auth.OTPValidationRequest):
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

@app.post("/a/auth/login/email")
def auth_login_email(login_request: schemas.auth.LoginEmailRequest):
    """
    Authenticates user with email and password.
    """
    res, code = authorization_manager.login_email_step(
        email=login_request.email
    )
    return {
        "success": res,
        "code": code,
        "redirect_url": "/login/password"
    }

@app.post("/a/auth/login/password")
def auth_login_password(login_request: schemas.auth.LoginPasswordRequest):
    """
    Authenticates user with email and password.
    """
    res, code = authorization_manager.verify_creds(
        email=login_request.email,
        password=login_request.password
    )
    if code == 404:
        return {
            "success": False,
            "code": code,
            "message": "User not found. Please register."
        }
    if code == 401:
        return {
            "success": False,
            "code": code,
            "message": "Invalid credentials."
        }
    if code != 200:
        return {
            "success": False,
            "code": code,
            "message": "An unknown error occurred."
        }
    auth_token = authorization_manager.generate_auth_token(
        user_id=login_request.email
    )
    return {
        "success": True,
        "code": 200,
        "auth_token": auth_token
    }

@app.post("/a/auth/login/register")
def auth_login_register(register_request: schemas.auth.LoginRegisterRequest):
    """
    Registers a new user with name, email and password.
    """
    _, code = authorization_manager.login_register(
        email=register_request.email,
        password=register_request.password
    )
    if code == 409:
        return {
            "success": False,
            "code": code,
            "message": "User already exists. Please login."
        }
    if code != 200:
        return {
            "success": False,
            "code": code,
            "message": "An unknown error occurred."
        }
    auth_token = authorization_manager.generate_auth_token(
        email=register_request.email
    )
    profile_manager.create_user_profile(
        email=register_request.email,
        full_name=register_request.full_name
    )
    return {
        "success": True,
        "code": 200,
        "auth_token": auth_token
    }

@app.post("/a/auth/verifyToken")
def auth_verify_token(verify_request: schemas.auth.VerifyTokenRequest):
    """
    Verifies auth token.
    """
    res, code = authorization_manager.verify_auth_token(
        auth_token=verify_request.auth_token
    )
    return {
        "success": res,
        "code": code
    }

@app.get("/a/profile/my")
def get_profile(Authorization: Annotated[str | None, Header()] = None):
    """
    Fetches user profile by email.
    """
    email, code = authorization_manager.verify_authorization_header(Authorization)
    if code != 200:
        return {
            "success": False,
            "code": code,
        }
    if not email:
        return {
            "success": False,
            "code": 404,
            "message": "Profile not found."
        }
    profile = profile_manager.get_user_profile(email=email)
    if not profile:
        return {
            "success": False,
            "code": 404,
            "message": "Profile not found."
        }
    return {
        "success": True,
        "code": 200,
        "profile": profile
    }
