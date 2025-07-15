from uuid import UUID
from pydantic import BaseModel
from models import PlatformEnum


class PlatformContactResponse(BaseModel):
    id: UUID
    contact_card_id: UUID
    platform: PlatformEnum
    platform_user_id: str


class PlatformContactCreate(BaseModel):
    contact_card_id: UUID
    platform: PlatformEnum
    platform_user_id: str


class PlatformContactUpdate(BaseModel):
    platform_user_id: str
