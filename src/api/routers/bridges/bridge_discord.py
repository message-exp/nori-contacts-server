from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_user_id_from_header
from schemas.bridge_discord import (
    LoginWithTokenRequest,
    LoginWithTokenResponse,
    LoginWithQrcodeResponse,
    LogoutResponse,
    PingResponse,
)
from services.bridge_discord_service import bridge_discord_service

router = APIRouter(tags=["Mautrix Discord"])


@router.get("/users/login/qrcode", response_model=LoginWithQrcodeResponse)
async def login_with_qr(user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_discord_service.login_with_qr(user_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/users/logout", response_model=LogoutResponse)
async def logout(user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_discord_service.logout(user_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.get("/users/info", response_model=PingResponse)
async def ping(user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_discord_service.ping(user_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/users/login/token", response_model=LoginWithTokenResponse)
async def login_with_token(
    loginWithTokenRequest: LoginWithTokenRequest,
    user_id: str = Depends(get_user_id_from_header),
):
    data, status = await bridge_discord_service.login_with_token(
        loginWithTokenRequest.token, user_id, loginWithTokenRequest.token_type
    )
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data
