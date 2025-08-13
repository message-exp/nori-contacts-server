from fastapi import APIRouter

from api.routers import contact_card, platform_contact
from api.routers.bridges import bridge_telegram , bridge_discord

api_router = APIRouter()
api_router.include_router(contact_card.router, prefix="/contact-cards")
api_router.include_router(platform_contact.router, prefix="/platform-contacts")
api_router.include_router(bridge_telegram.router, prefix="/bridge/telegram")
api_router.include_router(bridge_discord.router, prefix="/bridge/discord")
