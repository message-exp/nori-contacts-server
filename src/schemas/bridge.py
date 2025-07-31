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