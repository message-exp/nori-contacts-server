from pydantic import BaseModel

class LoginWithQrcodeRequest(BaseModel):
    token : str
class LoginWithQrcodeResponse(BaseModel):
    message : str
class LogoutResponse(BaseModel):
    message : str
    