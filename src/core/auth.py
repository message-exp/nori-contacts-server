from services.external_api import verify_token
from fastapi import HTTPException, status


async def authenticate_user(token: str) -> str:
    data, status_code = await verify_token(token)
    if status_code == 200 and isinstance(data, dict):
        user_id = data.get("user_id")
        if user_id:
            return user_id

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
    )
