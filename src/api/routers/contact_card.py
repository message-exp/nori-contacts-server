from uuid import UUID
from fastapi import APIRouter, Depends
from schemas.contact_card import (
    ContactCardResponse,
    ContactCardCreate,
    ContactCardUpdate,
)
from db.session import get_db
from api.dependencies import get_user_id_from_header
from services.contact_card_service import ContactCardServicer
from schemas.basic import MessageResponse
import asyncpg

router = APIRouter(tags=["Contact Card"])
service = ContactCardServicer()


@router.get("/", response_model=list[ContactCardResponse])
async def get_all_contact_cards(
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.get_all_contact_cards(db, user_id)


@router.post(
    "/",
    response_model=ContactCardResponse,
)
async def create_contact_card(
    contact: ContactCardCreate,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.create_contact_card(db, user_id, contact)


@router.put(
    "/{contact_card_id}",
    response_model=ContactCardResponse,
)
async def update_contact_card(
    contact_card_id: UUID,
    contact: ContactCardUpdate,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    return await service.update_contact_card(db, user_id, contact_card_id, contact)


@router.delete(
    "/{contact_card_id}",
    response_model=MessageResponse,
)
async def delete_contact_card(
    contact_card_id: UUID,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    await service.delete_contact_card(db, user_id, contact_card_id)
    return {"message": "success"}
