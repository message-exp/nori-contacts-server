import aiohttp
import json
from typing import Any
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
                    except(json.JSONDecodeError, aiohttp.ContentTypeError):
                        response_text = await response.text()
                        response_data = {"message": response_text}
                    return response_data, response.status
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}, 500


    async def login_with_qr(self , user_id : str) -> tuple[dict[str, Any], int]:
        #http or https
        websocket_url = f"{self.base_url.replace('https://', 'wss://').replace('http://', 'ws://')}/_matrix/provision/v1/login/qr?user_id={user_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(websocket_url, headers=self.headers) as ws:
                    message = await ws.receive()
                    message_data = json.loads(message.data)
                    return message_data , 200
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"internal server error: {e}")
    async def logout(self, user_id: str) -> tuple[dict[str, Any], int]:
        return await self._make_request('POST', f"/logout?user_id={user_id}")
    async def ping(self , user_id : str) -> tuple[dict[str, Any], int]:
        return await self._make_request('GET' , f"/ping?user_id={user_id}")
    async def login_with_token(self , token : str, user_id : str, token_type : str) -> tuple[dict[str, Any], int]:
        if token_type not in ["Bot" , "oauth" , "User"]:
            return {"error": "Invalid token type"}, 400
        match token_type:
            case "Bot":
                data = {"token": f"Bot {token}"}
            case "oauth":
                data = {"token": f"Bearer {token}"}
            case "User":
                data = {"token": f"{token}"}
        return await self._make_request('POST' , f"/login/token?user_id={user_id}" , data)
        
bridge_discord_service = BridgeDiscordService()