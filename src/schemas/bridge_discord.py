from pydantic import BaseModel

class LoginWithTokenRequest(BaseModel):
    token : str
    token_type : str
class LoginWithTokenResponse(BaseModel):
    success : bool
    id : str | None = None
    username : str | None = None
    discriminator : str | None = None
    error : str | None = None
    errcode : str | None = None
class LoginWithQrcodeResponse(BaseModel):
    code : str | None = None
    timeout : int | None = None
class LogoutResponse(BaseModel):
    success : bool
    status : str | None = None


class Conn(BaseModel):
    last_heartbeat_ack : int | None = None
    last_heartbeat_sent : int | None = None
class DiscordInfo(BaseModel):
    logged_in: bool
    connected : bool
    conn : Conn
class PingResponse(BaseModel):
    Discord: DiscordInfo
    mxid : str
    management_room : str
