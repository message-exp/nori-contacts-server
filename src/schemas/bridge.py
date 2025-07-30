from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str | None = None
class LoginRequest(BaseModel):
    phone: str | None = None