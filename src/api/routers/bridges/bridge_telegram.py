from fastapi import APIRouter, HTTPException , Depends
from services.bridge_telegram_service import bridge_telegram_service
from schemas.bridge import (
    LoginRequest,
    CodeRequest
)
from api.dependencies import get_user_id_from_header

router = APIRouter(tags=["Mautrix Telegram"])

@router.get("/users/info")
async def get_user_info(user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_telegram_service.get_user_info(user_id)
    
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    
    return data

@router.post("/users/login_request_code")
async def login_user(login_request: LoginRequest , user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_telegram_service.login_request_code(
        user_id, 
        login_request.phone
    )
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/users/login_send_code")
async def send_verification_code(code_request: CodeRequest, user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_telegram_service.login_send_code(
        user_id, 
        code_request.code
    )
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/users/logout")
async def logout_user(user_id: str = Depends(get_user_id_from_header)):
    data, status = await bridge_telegram_service.logout_user(user_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data