import asyncio
import json
from fastapi import APIRouter, Request, Depends
from api.dependencies import get_user_id_from_header
from schemas.bridge_discord import LoginWithTokenRequest ,LoginWithTokenResponse , LoginWithQrcodeResponse , LogoutResponse , PingResponse
from services.bridge_discord_service import bridge_discord_service

router = APIRouter(tags = ["Mautrix Discord"])

@router.get("/login/qrcode" , response_model = LoginWithQrcodeResponse)
async def login_with_qr(user_id: str = Depends(get_user_id_from_header)):
    data = await bridge_discord_service.login_with_qr(user_id)
    return data
@router.post("/logout", response_model = LogoutResponse)
async def logout(user_id: str = Depends(get_user_id_from_header)):
    data , status = await bridge_discord_service.logout(user_id)
    return data
@router.get("/ping" , response_model = PingResponse)
async def ping(user_id : str = Depends(get_user_id_from_header)):
    data , status = await bridge_discord_service.ping(user_id)
    return data
@router.post("/login/token" , response_model = LoginWithTokenResponse)
async def login_with_token(loginWithTokenRequest : LoginWithTokenRequest , user_id: str = Depends(get_user_id_from_header)):
    data , status = await bridge_discord_service.login_with_token(loginWithTokenRequest.token , user_id , loginWithTokenRequest.token_type)
    return data
