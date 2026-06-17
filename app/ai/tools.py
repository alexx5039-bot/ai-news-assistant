from __future__ import annotations

from langchain.tools import tool

from app.core.config import settings
from app.db.dependencies import get_article_service
from app.db.enums import ArticleStatus
from app.db.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate, ArticleUpdate
from app.services.news import NewsService


@tool
async def create_article(
        title: str,
        content: str
):
    """
    Create a new article
    """
    async with get_article_service() as service:

        article_create = ArticleCreate(
            title=title,
            content=content
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
    async with get_article_service() as service:


        article = await service.get_article(
            article_id
        )

        return ArticleResponse.model_validate(article).model_dump()


@tool
async def get_articles(
    limit: int = 10,
    offset: int = 0,
    status: ArticleStatus | None = None,
) -> list[dict]:
    """
    Get articles with optional pagination and status filter.
    """

    async with get_article_service() as service:

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

@tool
async def update_article_status(
    article_id: int,
    status: ArticleStatus,
) -> dict:
    """
    Update article status.
    """

    async with get_article_service() as service:

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
    async with get_article_service() as service:


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
    async with get_article_service() as service:


        await service.delete_article(
            article_id,
        )
        return {
            "success": True,
            "message": f"Article {article_id} deleted"
        }


@tool
async def search_news(query: str) -> str:
    """
    Search latest news by topic
    """
    news_service = NewsService(settings.gnews_api_key)
    result = await news_service.search_news(query)
    articles = result.get("articles", [])
    if not articles:
        return "No news found"

    return "\n".join(
        f"Title: {article['title']}\n"
        f"Description: {article.get('description', '')}"
        for article in articles[:5]
    )
