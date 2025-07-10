from fastapi import Depends
from core.auth import authenticate_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_user_id_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    return await authenticate_user(token)
