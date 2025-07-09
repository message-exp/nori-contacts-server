import aiohttp
from core.config import settings


async def verify_token(token: str) -> tuple:
    async with aiohttp.ClientSession() as session:
        url = f"https://{settings.MATRIX_SERVER}/_matrix/client/v3/account/whoami"
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(url, headers=headers) as res:
            data = await res.json()
            status = res.status
            return data, status
