# 在你的 FastAPI router 檔案中
import asyncio
import json
from fastapi import APIRouter, Request, Depends
from api.dependencies import get_user_id_from_header
# 舊的 import 可以移除或註解掉
# import websockets 
# 引入 aiohttp
import aiohttp
from fastapi import FastAPI, HTTPException, Query
from services.bridge_discord_service import bridge_discord_service

router = APIRouter(tags = ["Mautrix Discord"])

@router.get("/login-qrcode")
async def login(user_id: str = "@barney:tomorin.com"):
    return await bridge_discord_service.login(user_id)
@router.post("/logout")
async def logout(user_id: str = "@barney:tomorin.com"):
    return await bridge_discord_service.logout(user_id)