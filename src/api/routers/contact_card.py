from fastapi import APIRouter, Depends
from schemas.contact_card import ContactCardResponse, ContactCardCreate
from db.session import get_db
from api.dependencies import get_user_id_from_header
from services.contact_card_service import ContactCardServicer
from schemas.basic import ErrorResponse, MessageResponse
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
    responses={
        409: {
            "model": ErrorResponse,
            "description": "Conflict - contact already exists",
        }
    },
    response_model=MessageResponse,
)
async def create_contact_card(
    contact: ContactCardCreate,
    db: asyncpg.Connection = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
):
    await service.create_contact_card(db, user_id, contact)
    return {"message": "success"}
