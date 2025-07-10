from fastapi import APIRouter

from api.routers import contact_card

api_router = APIRouter()
api_router.include_router(contact_card.router, prefix="/contact-cards")
