import aiohttp
import json
from typing import Any, AsyncGenerator
from core.config import settings
from fastapi import HTTPException
class BridgeDiscordService:
    def __init__(self):
        self.base_url = settings.BRIDGE_DISCORD_URL
        self.shared_secret = settings.BRIDGE_DISCORD_SHARED_SECRET
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


    async def login_with_qr(self , user_id : str | None = None):
        #http or https
        websocket_url = f"{self.base_url.replace("http", "ws")}/_matrix/provision/v1/login/qr?user_id={user_id}"
        # print(f"WebSocket URL: {websocket_url}")
        # websocket_url = f"{websocket_url}?user_id={user_id}"
        # print(f"full websocket URL: {websocket_url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(websocket_url, headers=self.headers) as ws:
                    message = await ws.receive()
                    message_str = message.data
                    # if message_str[success]
                    message_data = json.loads(message_str)
                    # print(f"message_data :{message_data.get("success")}")
                    # return message_data
                    # if message_data.get("success") is False:
                    #     return message_data
                    return message_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"internal server error: {e}")
    async def logout(self, user_id: str | None = None) -> dict[str, Any]:
        return await self._make_request('POST', f"/logout?user_id={user_id}")
    async def ping(self):
        return await self._make_request('GET' , "/ping")
    async def login_with_token(token : str | None = None , user_id : str | None = None):
        data = {"token": token}
        return await self._make_request('POST' , "/login/token" , data)
        

bridge_discord_service = BridgeDiscordService()