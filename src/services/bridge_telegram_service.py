import aiohttp
from typing import Any
from core.config import settings

class BridgeTelegramService:
    
    def __init__(self):
        self.base_url = settings.BRIDGE_TELEGRAM_URL
        self.shared_secret = settings.BRIDGE_TELEGRAM_SHARED_SECRET
        self.white_listed_url = settings.BRIDGE_WHITE_LISTED_URL
        self.headers = {
            "Authorization": f"Bearer {self.shared_secret}",
            "Content-Type": "application/json"
        }
    async def _make_request(
        self, 
        method: str | None = None, 
        endpoint: str | None = None, 
        data: dict[str, Any]  | None = None
    ) -> tuple[dict[str, Any], int]:
        if self.base_url != self.white_listed_url:
            return {"error": "BRIDGE_TELEGRAM_URL is not in white list."}, 500
        url = f"{self.base_url}/_matrix/provision/v1{endpoint}"
        print(f"Making {method} request to: {url}")
                             
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data
                ) as response:
                    try:
                        response_data = await response.json()
                    except:
                        response_text = await response.text()
                        response_data = {"message": response_text}
                    return response_data, response.status
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}, 500

    async def get_user_info(self, user_id: str | None = None) -> tuple[dict[str, Any], int]:
        return await self._make_request("GET", f"/user/{user_id}")

    async def login_request_code(self, user_id: str | None = None, phone_number: str | None = None) -> tuple[dict[str, Any], int]:
        data = {"phone": phone_number}
        return await self._make_request("POST", f"/user/{user_id}/login/request_code", data)

    async def login_send_code(self, user_id: str | None = None, code: str | None = None) -> tuple[dict[str, Any], int]:
        data = {"code": code}
        return await self._make_request("POST", f"/user/{user_id}/login/send_code", data)

    async def logout_user(self, user_id: str | None = None) -> tuple[dict[str, Any], int]:
        return await self._make_request("POST", f"/user/{user_id}/logout")

bridge_telegram_service = BridgeTelegramService()