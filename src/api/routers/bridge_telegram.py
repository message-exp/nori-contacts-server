from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from services.bridge_telegram_service import bridge_telegram_service

router = APIRouter(prefix="/mautrix-telegram", tags=["Mautrix Telegram"])

class CodeRequest(BaseModel):
    code: str
class LoginRequest(BaseModel):
    phone: str

@router.get("/user/{user_id}/info")
async def get_user_info(user_id: str):
    data, status = await bridge_telegram_service.get_user_info(user_id)
    
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    
    return data

@router.post("/user/{user_id}/login_request_code")
async def login_user(user_id: str, login_request: LoginRequest):
    data, status = await bridge_telegram_service.login_request_code(
        user_id, 
        login_request.phone
    )
    
    if status not in [200, 202]:  # 202 可能表示需要驗證碼
        raise HTTPException(status_code=status, detail=data)
    
    return data


@router.post("/user/{user_id}/login_send_code")
async def send_verification_code(user_id: str, code_request: CodeRequest):
    data, status = await bridge_telegram_service.login_send_code(
        user_id, 
        code_request.code
    )
    
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    
    return data


@router.post("/user/{user_id}/logout")
async def logout_user(user_id: str):
    data, status = await bridge_telegram_service.logout_user(user_id)
    
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    
    return data