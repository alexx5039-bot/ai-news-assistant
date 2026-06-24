from __future__ import annotations

import traceback

import requests
from langchain.tools import tool

from app.core.config import settings
from app.db.dependencies import get_article_service, get_article_service_context
from app.db.enums import ArticleStatus
from app.db.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate, ArticleUpdate



@tool
async def create_article(
        title: str,
        content: str,
        summary: str
):
    """
    Create a new article
    """
    async with get_article_service_context() as service:

        article_create = ArticleCreate(
            title=title,
            content=content,
            summary=summary
        )
        article = await service.create_article(
            article_create
        )

        return ArticleResponse.model_validate(article).model_dump()

@tool
async def get_article(
        article_id: int,
) -> dict:
    """
    Get article with provided id
    """
    async with get_article_service_context() as service:


        article = await service.get_article(
            article_id
        )

        return ArticleResponse.model_validate(article).model_dump()


@tool
async def get_articles(
    limit: int = 50,
    offset: int = 0,
    status: ArticleStatus | None = None,
) -> list[dict]:
    """
    Retrieve an article by its ID.
    Returns title, content, status and metadata.
    """

    async with get_article_service_context() as service:

        try:
            articles = await service.get_articles(
                limit=limit,
                offset=offset,
                status=status,
            )

            return [
                ArticleResponse.model_validate(
                    article
                ).model_dump()
                for article in articles
            ]
        except Exception:
            traceback.print_exc()
            raise



@tool
async def update_article_status(
    article_id: int,
    status: ArticleStatus,
) -> dict:
    """
    Update article status.
    """

    async with get_article_service_context() as service:

        article = await service.update_status(
            article_id=article_id,
            status=status,
        )

        return ArticleResponse.model_validate(
            article
        ).model_dump()

@tool
async def update_article(
        article_id: int,
        article_data: ArticleUpdate
) -> dict:
    """
    Update article with provided id
    """
    async with get_article_service_context() as service:


        article = await service.update_article(
            article_id,
            article_data
        )

        return ArticleResponse.model_validate(article).model_dump()

@tool
async def delete_article(
        article_id: int,
):
    """
    Delete article with provided id
    """
    async with get_article_service_context() as service:


        await service.delete_article(
            article_id,
        )
        return {
            "success": True,
            "message": f"Article {article_id} deleted"
        }




@tool
async def search_news(query: str) -> dict:
    """
    Search recent news articles by topic.
    """

    response = requests.get(
        "https://gnews.io/api/v4/search",
        params={
            "q": query,
            "apikey": settings.gnews_api_key,
            "lang": "en",
            "max": 10,
        }
    )

    response.raise_for_status()

    articles = response.json()["articles"]

    news_text = "\n".join(
        f"Title: {article['title']}\n"
        f"Description: {article.get('description', '')}"
        for article in articles[:5]
    )

    return {
        "news": news_text,
        "sources": [
            {
                "title": article["title"],
                "url": article.get("url", "")
            }
            for article in articles[:5]
        ]
    }

@tool
async def create_article_source(
    article_id: int,
    title: str,
    url: str
):
    """
    Create article source.
    """

    async with get_article_service_context() as service:

        source = await service.create_source(
            article_id=article_id,
            title=title,
            url=url
        )

        return {
            "id": source.id
        }