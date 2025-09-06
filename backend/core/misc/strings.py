from dataclasses import dataclass

@dataclass
class StringsClass:
    pass

@dataclass
class Auth(StringsClass):
    otp_sms: str = "Your OTP is {otp}. It is valid for {ttl_str}. Do not share it with anyone."