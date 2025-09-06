from . import (
    database,
    config,
)
import core.misc.strings
from twilio.rest import Client
import string
import random
import secrets
import time
import humanize

class TwilioClient:
    """
    Twilio client wrapper.
    """
    def __init__(self, account_sid: str, auth_token: str, sms_from_ph: str):
        self.c = Client(account_sid, auth_token)
        self.sms_from_ph = sms_from_ph
    def send_sms(self, to: str, body: str):
        """
        Sends SMS using Twilio API.
        """
        self.c.messages.create(
            body = body,
            from_=self.sms_from_ph,
            to=to
        )

class OTPSession:
    """
    Manages OTP sessions.
    Generates, sends and verifies OTPs.
    """
    def __init__(
            self,
            twilio_client: TwilioClient,
            db: database.pymongo.database.Database,
            auth_strings: core.misc.strings.Auth,
            phone_number: str | None = None,
            session_id: str | None = None,
            ttl: int = 300,
            length: int = 4):
        self.twilio_client = twilio_client
        self.db = db
        self.length = length
        self.ttl = ttl
        self.auth_strings = auth_strings
        if phone_number:
            self.phone_number = phone_number
            self.session_id = secrets.token_hex(16)
        else:
            self.session_id = session_id
    def _generate_otp(self, length=4) -> str:
        otp = ''.join(random.choice(string.digits) for _ in range(length))
        return otp
    def _save_otp_session(self, otp: str):
        self.db["otp_sessions"].insert_one(
            {
                "phone": self.phone_number, 
                "otp": otp,
                "session_id": self.session_id,
                "created_at": time.time(),
                "attempts": 0
            }
        )
    def send_otp(self):
        """
        Generates and sends OTP to user's phone number.
        """
        otp = self._generate_otp()
        self._save_otp_session(otp)
        sms_body = self.auth_strings.otp_sms.format(
            otp=otp,
            ttl_str=humanize.naturaldelta(self.ttl)
        )
        self.twilio_client.send_sms(
            body=sms_body,
            to=self.phone_number
        )
        return self.session_id
    def verify_otp(self, otp: str):
        """
        Verifies OTP for the session.
        """
        data = self.db["otp_sessions"].find_one({"session_id": self.session_id})
        if data is None:
            return False, 404
        if data.get("otp") != otp:
            if data.get("attempts", 0) >= 3:
                return False, 429
            self.db["otp_sessions"].update_one({"session_id": self.session_id}, {"$inc": {"attempts": 1}})
            return False, 401
        if data.get("created_at", time.time()-self.ttl)+self.ttl > time.time():
            return True, 200
        return False, 401

class AuthorizationManager:
    """
    Handles user authentication.
    """
    def __init__(
            self,
            config: config.Auth,
            db: database.pymongo.database.Database,
            twilio_client: TwilioClient
        ):
        self.config = config
        self.auth_strings = core.misc.strings.Auth()
        self.db = db
        self.twilio_client = twilio_client
    def otp_factory(
            self,
            phone_number: str | None = None,
            session_id: str | None= None
        ) -> OTPSession:
        return OTPSession(
            twilio_client=self.twilio_client,
            db=self.db,
            auth_strings=self.auth_strings,
            phone_number=phone_number,
            session_id=session_id,
            ttl=self.config.login_otp_ttl
        )
