from uuid import UUID
import asyncpg
from fastapi import HTTPException, status
from db.repositories.contact_cards_repository import (
    get_single_contact_card_by_id_and_owner,
)
from schemas.platform_contact import (
    PlatformContactCreate,
    PlatformContactUpdate,
)
from models import PlatformContact
from db.repositories.platform_contact_repository import (
    get_platform_contacts_by_contact_card_id,
    insert_platform_contact,
    update_platform_contact_user_id,
    delete_platform_contact,
    get_platform_contacts_by_contact_card_id_and_platform,
)


class PlatformContactServicer:
    async def get_platform_contacts(
        self, db: asyncpg.Connection, user_id: str, contact_card_id: UUID
    ):
        record = await get_single_contact_card_by_id_and_owner(
            db, contact_card_id, user_id
        )
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact card not found."
            )
        return await get_platform_contacts_by_contact_card_id(db, contact_card_id)

    async def create_platform_contact(
        self,
        db: asyncpg.Connection,
        user_id: str,
        platform_contact: PlatformContactCreate,
    ) -> PlatformContact:
        contact_card = await get_single_contact_card_by_id_and_owner(
            db, platform_contact.contact_card_id, user_id
        )
        if not contact_card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact card not found."
            )
        new_platform_contact = await insert_platform_contact(
            db,
            platform_contact.contact_card_id,
            platform_contact.platform,
            platform_contact.platform_user_id,
        )
        if not new_platform_contact:
            raise HTTPException(status_code=409, detail="Platform contact already exists.")
        return new_platform_contact
    async def update_platform_contact(
        self,
        db: asyncpg.Connection,
        user_id: str,
        contact_card_id: UUID,
        platform: str,
        platform_contact: PlatformContactUpdate,
    ):
        contact_card = await get_single_contact_card_by_id_and_owner(
            db, contact_card_id, user_id
        )
        if not contact_card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact card not found."
            )
        old_platform_contact = (
            await get_platform_contacts_by_contact_card_id_and_platform(
                db, contact_card_id, platform
            )
        )
        if old_platform_contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Platform contact not found.",
            )
        updated_platform_contact = await update_platform_contact_user_id(
            db, contact_card_id, platform, platform_contact.platform_user_id
        )
        if updated_platform_contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Platform contact not found.",
            )
        return updated_platform_contact

    async def delete_platform_contacts(
        self,
        db: asyncpg.Connection,
        user_id: str,
        contact_card_id: UUID,
        platform: str,
    ):
        record = await get_single_contact_card_by_id_and_owner(
            db, contact_card_id, user_id
        )
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact card not found."
            )
        old_platform_contact = (
            await get_platform_contacts_by_contact_card_id_and_platform(
                db, contact_card_id, platform
            )
        )
        if old_platform_contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Platform contact not found.",
            )
        await delete_platform_contact(db, contact_card_id, platform)
