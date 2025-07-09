from enum import Enum
from pydantic import BaseModel


class PlatformEnum(str, Enum):
    TELEGRAM = "Telegram"
    DISCORD = "Discord"


class ContactCard(BaseModel):
    contact_name: str
    contact_avatar_url: str | None = None


class PlatformContact(BaseModel):
    contact_card_id: int
    platform: PlatformEnum
    platform_user_id: str
