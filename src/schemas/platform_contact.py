from uuid import UUID
from pydantic import BaseModel
from models import PlatformEnum


class PlatformContactResponse(BaseModel):
    id: UUID
    contact_card_id: UUID
    platform: PlatformEnum
    dm_room_id: str
    platform_user_id: str


class PlatformContactCreate(BaseModel):
    contact_card_id: UUID
    platform: PlatformEnum
    dm_room_id: str
    platform_user_id: str


class PlatformContactUpdate(BaseModel):
    dm_room_id: str
    platform_user_id: str
