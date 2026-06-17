import httpx
from app.core.config import settings


class NewsService:
    def __init__(self, api_key: str):
        self.api_key = settings.gnews_api_key

    async def search_news(self, query: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://gnews.io/api/v4/search",
                params={
                    "q": query,
                    "lang": "en",
                    "apikey": self.api_key,
                    "max": 10,
                },
            )
            response.raise_for_status()
            return response.json()