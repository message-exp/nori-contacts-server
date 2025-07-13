import asyncpg
from schemas.contact_card import ContactCardCreate
from db.repositories.contact_cards_repository import (
    get_contact_cards_by_owner,
    insert_contact_card,
)


class ContactCardServicer:
    async def get_all_contact_cards(self, db: asyncpg.Connection, user_id: str):
        return await get_contact_cards_by_owner(db, user_id)

    async def create_contact_card(
        self, db: asyncpg.Connection, user_id: str, contact: ContactCardCreate
    ):
        await insert_contact_card(
            db, user_id, contact.contact_name,contact.nickname ,contact.contact_avatar_url
        )
