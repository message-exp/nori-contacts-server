from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from typing import Annotated

ValidatedPhone = Annotated[
    str,
    PhoneNumberValidator(
        default_region='TW',
        number_format='E164'
    ),
]

class CodeRequest(BaseModel):
    code: str
class LoginRequest(BaseModel):
    phone: ValidatedPhone


class TelegramInfo(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str
    is_bot: bool

class UserInfoResponse(BaseModel):
    telegram: TelegramInfo | None = None
    mxid: str
    permissions: str

class MessageResponse(BaseModel):
    message: str

class SendVerifyCodeResponse(BaseModel):
    state: str
    username: str | None = None
    phone: str