from aiogram import Router
from aiogram.types import Message
import httpx

from app.core.config import settings

router = Router()

@router.message()
async def chat(message: Message):
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.api_url}/ai/chat",
            json={"message": message.text}
        )

    data = response.json()

    await message.answer(data["response"])