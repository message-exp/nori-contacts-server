from pydantic import BaseModel

class CodeRequest(BaseModel):
    code: str
class LoginRequest(BaseModel):
    phone: str