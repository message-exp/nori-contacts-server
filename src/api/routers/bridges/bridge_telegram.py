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

@router.post("/users/login/code")
async def login_user(login_request: LoginRequest , user_id: str = Depends(get_user_id_from_header)):
    """
    Request Telegram verification code to start login process
    
    This endpoint sends a Telegram verification code to the user's phone number.
    
    - **phone**: User's phone number (must include country code, e.g., +886912345678)
    - **user_id**: Current authenticated user's Matrix ID (automatically extracted from token)
    
    **Process flow:**
    1. Provide phone number with country code
    2. Telegram will send a verification code to that number
    3. Use `/users/login/code/verify` endpoint to submit the verification code
    
    **Phone number format:**
    - Must include country code (e.g., +886 for Taiwan)
    - Example: +886912345678
    """
    data, status = await bridge_telegram_service.login_request_code(
        user_id, 
        login_request.phone
    )
    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    return data


@router.post("/users/login/code/verify")
async def send_verification_code(code_request: CodeRequest, user_id: str = Depends(get_user_id_from_header)):
    """
    Submit Telegram verification code to complete login
    
    After receiving the Telegram verification code, use this endpoint to complete the login process.
    
    - **code**: Verification code received from Telegram (usually 5-6 digits)
    - **user_id**: Current authenticated user's Matrix ID (automatically extracted from token)
    
    **Upon success:**
    - Establishes Telegram to Matrix bridge connection
    - Starts syncing Telegram messages to Matrix
    """
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