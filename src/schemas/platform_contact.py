from pydantic import BaseModel
from models import PlatformEnum


class PlatformContactResponse(BaseModel):
    contact_card_id: int
    platform: PlatformEnum
    platform_user_id: str
