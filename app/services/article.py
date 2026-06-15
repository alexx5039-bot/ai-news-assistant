from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException

from app.db.enums import ArticleStatus
from app.db.models import Article
from app.repositories.article import ArticleRepository
from app.schemas.article import ArticleCreate, ArticleUpdate


class ArticleService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    async def create_article(
            self,
            article_data: ArticleCreate
    ) -> Article:
        return await self.repository.create(
            article_data
        )

    async def get_article(self, article_id: int) -> Article:
        article = await self.repository.get_article_by_id(article_id)
        if article is None:
            raise HTTPException(
                status_code=404,
                detail="Article is not found"
            )

        return article


    async def get_articles(self,
                           limit: int = 10,
                           offset: int = 0,
                           status: ArticleStatus | None = None
    ) -> Sequence[Article]:
        articles = await self.repository.get_articles(
            limit=limit,
            offset=offset,
            status=status
        )

        return articles

    async def delete_article(self, article_id):
        article = await self.repository.get_article_by_id(article_id)

        if article is None:
            raise HTTPException(
                status_code=404,
                detail="Article is not found"
            )

        await self.repository.delete_article(article)


    async def update_article(self, article_id: int, article_data: ArticleUpdate) -> Article:
        article = await self.repository.get_article_by_id(article_id)

        if article is None:
            raise HTTPException(
                status_code=404,
                detail="Article is not found"
            )
        updated_data = article_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(article, field, value)
        await self.repository.update_article(article)

        return article

    async def update_status(self,
                            article_id: int,
                            status: ArticleStatus
    ) -> Article:

        article = await self.repository.get_article_by_id(article_id)

        if article is None:
            raise HTTPException(
                status_code=404,
                detail="Article not found"
            )

        if (
                article.status == ArticleStatus.ARCHIVED
                and status == ArticleStatus.DRAFT
        ):
            raise HTTPException(
                status_code=400,
                detail="Archived article cannot be returned to draft"
            )

        article.status = status

        return await self.repository.update_article(article)
