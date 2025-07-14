from uuid import UUID
from fastapi import APIRouter, Depends
from schemas.platform_contact import (
    PlatformContactCreate,
    PlatformContactResponse,
    PlatformContactUpdate,
    PlatformEnum
)
from db.session import get_db
from api.dependencies import get_user_id_from_header
from services.platform_contact_service import PlatformContactServicer
from schemas.basic import MessageResponse
import asyncpg

router = APIRouter(tags=["Platform contact"])
service = PlatformContactServicer()


@router.get("/{contact_card_id}", response_model=list[PlatformContactResponse])
async def get_platform_contacts(
    contact_card_id: UUID,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.get_platform_contacts(db, user_id, contact_card_id)


@router.post(
    "/",
    response_model=PlatformContactResponse,
)
async def create_platform_contact(
    platform_contact: PlatformContactCreate,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.create_platform_contact(db, user_id, platform_contact)


@router.put(
    "/{contact_card_id}/{platform}",
    response_model=PlatformContactResponse,
)
async def update_platform_contact(
    contact_card_id: UUID,
    platform: PlatformEnum,
    platform_contact: PlatformContactUpdate,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.update_platform_contact(
        db, user_id, contact_card_id, platform, platform_contact
    )


@router.delete(
    "/{contact_card_id}/{platform}",
    response_model=MessageResponse,
)
async def delete_platform_contact(
    contact_card_id: UUID,
    platform: PlatformEnum,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    await service.delete_platform_contacts(db, user_id, contact_card_id, platform)
    return {"message": "success"}
