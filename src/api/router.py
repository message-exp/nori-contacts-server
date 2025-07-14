from fastapi import APIRouter

from api.routers import contact_card, platform_contact

api_router = APIRouter()
api_router.include_router(contact_card.router, prefix="/contact-cards")
api_router.include_router(platform_contact.router, prefix="/platform-contacts")
