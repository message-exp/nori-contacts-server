from enum import Enum
from pydantic import BaseModel


class PlatfromEnum(str, Enum):
    TELEGRAM = "Telegram"
    DISCORD = "Discord"


class UserContact(BaseModel):
    user_id: str
    platfrom_user_id: str
    platfrom_username: str
    platfrom: PlatfromEnum
    avatar: str | None = None
